#!/usr/bin/env python
import argparse
from typing import Tuple, Dict

import zmq
import os
import sys
import platform
import random
import time
import pickle
import logging
import queue
import threading
import json
import daemon
import collections

from parsl.executors.errors import ScalingFailed
from parsl.version import VERSION as PARSL_VERSION

from funcx_endpoint.executors.high_throughput.messages import Message, COMMAND_TYPES, MessageType, Task
from funcx_endpoint.executors.high_throughput.messages import EPStatusReport, Heartbeat, TaskStatusCode
from funcx.sdk.client import FuncXClient
from funcx_endpoint.executors.high_throughput.interchange_task_dispatch import naive_interchange_task_dispatch
from funcx.serialize import FuncXSerializer
from funcx_endpoint.executors.high_throughput.taskqueue import TaskQueue

LOOP_SLOWDOWN = 0.0  # in seconds
HEARTBEAT_CODE = (2 ** 32) - 1
PKL_HEARTBEAT_CODE = pickle.dumps(HEARTBEAT_CODE)


class ShutdownRequest(Exception):
    """ Exception raised when any async component receives a ShutdownRequest
    """

    def __init__(self):
        self.tstamp = time.time()

    def __repr__(self):
        return "Shutdown request received at {}".format(self.tstamp)


class ManagerLost(Exception):
    """ Task lost due to worker loss. Worker is considered lost when multiple heartbeats
    have been missed.
    """

    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.tstamp = time.time()

    def __repr__(self):
        return "Task failure due to loss of worker {}".format(self.worker_id)


class BadRegistration(Exception):
    ''' A new Manager tried to join the executor with a BadRegistration message
    '''

    def __init__(self, worker_id, critical=False):
        self.worker_id = worker_id
        self.tstamp = time.time()
        self.handled = "critical" if critical else "suppressed"

    def __repr__(self):
        return "Manager:{} caused a {} failure".format(self.worker_id,
                                                       self.handled)


class Interchange(object):
    """ Interchange is a task orchestrator for distributed systems.

    1. Asynchronously queue large volume of tasks (>100K)
    2. Allow for workers to join and leave the union
    3. Detect workers that have failed using heartbeats
    4. Service single and batch requests from workers
    5. Be aware of requests worker resource capacity,
       eg. schedule only jobs that fit into walltime.

    TODO: We most likely need a PUB channel to send out global commandzs, like shutdown
    """

    def __init__(self,
                 config,
                 client_address="127.0.0.1",
                 interchange_address="127.0.0.1",
                 client_ports: Tuple[int, int, int] = (50055, 50056, 50057),
                 worker_ports=None,
                 worker_port_range=(54000, 55000),
                 cores_per_worker=1.0,
                 launch_cmd=None,
                 logdir=".",
                 logging_level=logging.INFO,
                 endpoint_id=None,
                 suppress_failure=False,
                 ):
        """
        Parameters
        ----------
        config : funcx.Config object
             Funcx config object that describes how compute should be provisioned

        client_address : str
             The ip address at which the parsl client can be reached. Default: "127.0.0.1"

        interchange_address : str
             The ip address at which the workers will be able to reach the Interchange. Default: "127.0.0.1"

        client_ports : Tuple[int, int, int]
             The ports at which the client can be reached

        launch_cmd : str
             TODO : update

        worker_ports : tuple(int, int)
             The specific two ports at which workers will connect to the Interchange. Default: None

        worker_port_range : tuple(int, int)
             The interchange picks ports at random from the range which will be used by workers.
             This is overridden when the worker_ports option is set. Defauls: (54000, 55000)

        cores_per_worker : float
             cores to be assigned to each worker. Oversubscription is possible
             by setting cores_per_worker < 1.0. Default=1

        logdir : str
             Parsl log directory paths. Logs and temp files go here. Default: '.'

        logging_level : int
             Logging level as defined in the logging module. Default: logging.INFO (20)

        endpoint_id : str
             Identity string that identifies the endpoint to the broker

        suppress_failure : Bool
             When set to True, the interchange will attempt to suppress failures. Default: False
        """
        self.logdir = logdir
        try:
            os.makedirs(self.logdir)
        except FileExistsError:
            pass

        start_file_logger("{}/interchange.log".format(self.logdir), level=logging_level)
        logger.info("logger location {}".format(logger.handlers))
        logger.info("Initializing Interchange process with Endpoint ID: {}".format(endpoint_id))
        self.config = config
        logger.info("Got config : {}".format(config))

        self.strategy = self.config.strategy
        self.client_address = client_address
        self.interchange_address = interchange_address
        self.suppress_failure = suppress_failure

        self.poll_period = self.config.poll_period
        self.heartbeat_period = self.config.heartbeat_period
        self.heartbeat_threshold = self.config.heartbeat_threshold
        # initalize the last heartbeat time to start the loop
        self.last_heartbeat = time.time()

        self.serializer = FuncXSerializer()
        logger.info("Attempting connection to client at {} on ports: {},{},{}".format(
            client_address, client_ports[0], client_ports[1], client_ports[2]))

        self.task_incoming = TaskQueue(client_address,
                                       port=client_ports[0],
                                       identity=endpoint_id,
                                       mode='client',
                                       set_hwm=0,
                                       RCVTIMEO=10)
        self.context = self.task_incoming.zmq_context()
        logger.info("Task incoming on tcp://{}:{}".format(client_address, client_ports[0]))

        self.results_outgoing = TaskQueue(client_address,
                                          port=client_ports[1],
                                          identity=endpoint_id,
                                          mode='client',
                                          set_hwm=0)

        self.command_channel = TaskQueue(client_address,
                                         port=client_ports[2],
                                         identity=endpoint_id,
                                         mode='client',
                                         RCVTIMEO=1000,  # in milliseconds
                                         set_hwm=0)

        # TODO :Register all channels with the authentication string.
        self.task_incoming.put('forwarder', b'')
        self.results_outgoing.put('forwarder', b'')
        self.command_channel.put('forwarder', b'')

        logger.info("Connected to client")

        self.pending_task_queue = {}
        self.containers = {}
        self.total_pending_task_count = 0
        self.fxs = FuncXClient()

        logger.info("Interchange address is {}".format(self.interchange_address))
        self.worker_ports = worker_ports
        self.worker_port_range = worker_port_range

        self.task_outgoing = self.context.socket(zmq.ROUTER)
        self.task_outgoing.set_hwm(0)
        self.results_incoming = self.context.socket(zmq.ROUTER)
        self.results_incoming.set_hwm(0)

        self.endpoint_id = endpoint_id
        if self.worker_ports:
            self.worker_task_port = self.worker_ports[0]
            self.worker_result_port = self.worker_ports[1]

            self.task_outgoing.bind("tcp://*:{}".format(self.worker_task_port))
            self.results_incoming.bind("tcp://*:{}".format(self.worker_result_port))

        else:
            self.worker_task_port = self.task_outgoing.bind_to_random_port('tcp://*',
                                                                           min_port=worker_port_range[0],
                                                                           max_port=worker_port_range[1], max_tries=100)
            self.worker_result_port = self.results_incoming.bind_to_random_port('tcp://*',
                                                                                min_port=worker_port_range[0],
                                                                                max_port=worker_port_range[1], max_tries=100)

        logger.info("Bound to ports {},{} for incoming worker connections".format(
            self.worker_task_port, self.worker_result_port))

        self._ready_manager_queue = {}

        self.blocks = {}  # type: Dict[str, str]
        self.block_id_map = {}
        self.launch_cmd = launch_cmd
        self.last_core_hr_counter = 0
        if not launch_cmd:
            self.launch_cmd = ("funcx-manager {debug} {max_workers} "
                               "-c {cores_per_worker} "
                               "--poll {poll_period} "
                               "--task_url={task_url} "
                               "--result_url={result_url} "
                               "--logdir={logdir} "
                               "--block_id={{block_id}} "
                               "--hb_period={heartbeat_period} "
                               "--hb_threshold={heartbeat_threshold} "
                               "--worker_mode={worker_mode} "
                               "--scheduler_mode={scheduler_mode} "
                               "--worker_type={{worker_type}} ")

        self.current_platform = {'parsl_v': PARSL_VERSION,
                                 'python_v': "{}.{}.{}".format(sys.version_info.major,
                                                               sys.version_info.minor,
                                                               sys.version_info.micro),
                                 'os': platform.system(),
                                 'hname': platform.node(),
                                 'dir': os.getcwd()}

        logger.info("Platform info: {}".format(self.current_platform))
        self._block_counter = 0
        try:
            self.load_config()
        except Exception:
            logger.exception("Caught exception")
            raise

        self.tasks = set()
        self.task_status_deltas = {}

    def load_config(self):
        """ Load the config
        """
        logger.info("Loading endpoint local config")
        working_dir = self.config.working_dir
        if self.config.working_dir is None:
            working_dir = "{}/{}".format(self.logdir, "worker_logs")
        logger.info("Setting working_dir: {}".format(working_dir))

        self.config.provider.script_dir = working_dir
        if hasattr(self.config.provider, 'channel'):
            self.config.provider.channel.script_dir = os.path.join(working_dir, 'submit_scripts')
            self.config.provider.channel.makedirs(self.config.provider.channel.script_dir, exist_ok=True)
            os.makedirs(self.config.provider.script_dir, exist_ok=True)

        debug_opts = "--debug" if self.config.worker_debug else ""
        max_workers = "" if self.config.max_workers_per_node == float('inf') \
                      else "--max_workers={}".format(self.config.max_workers_per_node)

        worker_task_url = f"tcp://{self.interchange_address}:{self.worker_task_port}"
        worker_result_url = f"tcp://{self.interchange_address}:{self.worker_result_port}"

        l_cmd = self.launch_cmd.format(debug=debug_opts,
                                       max_workers=max_workers,
                                       cores_per_worker=self.config.cores_per_worker,
                                       # mem_per_worker=self.config.mem_per_worker,
                                       prefetch_capacity=self.config.prefetch_capacity,
                                       task_url=worker_task_url,
                                       result_url=worker_result_url,
                                       nodes_per_block=self.config.provider.nodes_per_block,
                                       heartbeat_period=self.config.heartbeat_period,
                                       heartbeat_threshold=self.config.heartbeat_threshold,
                                       poll_period=self.config.poll_period,
                                       worker_mode=self.config.worker_mode,
                                       scheduler_mode=self.config.scheduler_mode,
                                       logdir=working_dir)
        self.launch_cmd = l_cmd
        logger.info("Launch command: {}".format(self.launch_cmd))

        if self.config.scaling_enabled:
            logger.info("Scaling ...")
            self.scale_out(self.config.provider.init_blocks)

    def get_tasks(self, count):
        """ Obtains a batch of tasks from the internal pending_task_queue

        Parameters
        ----------
        count: int
            Count of tasks to get from the queue

        Returns
        -------
        List of upto count tasks. May return fewer than count down to an empty list
            eg. [{'task_id':<x>, 'buffer':<buf>} ... ]
        """
        tasks = []
        for i in range(0, count):
            try:
                x = self.pending_task_queue.get(block=False)
            except queue.Empty:
                break
            else:
                tasks.append(x)

        return tasks

    def migrate_tasks_to_internal(self, kill_event, status_request):
        """Pull tasks from the incoming tasks 0mq pipe onto the internal
        pending task queue

        Parameters:
        -----------
        kill_event : threading.Event
              Event to let the thread know when it is time to die.
        """
        logger.info("[TASK_PULL_THREAD] Starting")
        task_counter = 0
        poller = zmq.Poller()
        poller.register(self.task_incoming, zmq.POLLIN)

        # TODO : Update this to be a proper registration message with client key
        # added to tie in auth.
        # msg = self.task_incoming.put('forwarder', b'hello from worker')
        while not kill_event.is_set():
            # Check when the last heartbeat was.
            # logger.debug(f"[TASK_PULL_THREAD] Last heartbeat: {self.last_heartbeat}")
            if int(time.time() - self.last_heartbeat) > self.heartbeat_threshold:
                logger.critical("[TASK_PULL_THREAD] Missed too many heartbeats. Setting kill event.")
                kill_event.set()
                break

            try:
                # TODO : Check the kwarg options for get
                msg = self.task_incoming.get()[0]
                self.last_heartbeat = time.time()
            except zmq.Again:
                # We just timed out while attempting to receive
                logger.debug("[TASK_PULL_THREAD] {} tasks in internal queue".format(self.total_pending_task_count))
                continue

            try:
                msg = Message.unpack(msg)
                logger.debug("[TASK_PULL_THREAD] received Message/Heartbeat? on task queue")
            except Exception:
                logger.exception("Failed to unpack message from forwarder")
                pass

            if msg == 'STOP':
                kill_event.set()
                break
            elif isinstance(msg, Heartbeat):
                logger.info("Got heartbeat")

            elif isinstance(msg, Task):
                logger.info("[TASK_PULL_THREAD] Received task:{}".format(msg))
                self.get_container(msg.container_id)
                if msg.container_id not in self.pending_task_queue:
                    self.pending_task_queue[msg.container_id] = queue.Queue(maxsize=10 ** 6)

                self.pending_task_queue[msg.container_id].put(msg)
                self.total_pending_task_count += 1
                self.task_status_deltas[msg.task_id] = TaskStatusCode.WAITING_FOR_NODES
                logger.debug(f"[TASK_PULL_THREAD] task {msg.task_id} is now WAITING_FOR_NODES")
                logger.debug("[TASK_PULL_THREAD] pending task count: {}".format(self.total_pending_task_count))
                task_counter += 1
                logger.debug("[TASK_PULL_THREAD] Fetched task:{}".format(task_counter))

    def get_container(self, container_uuid):
        """ Get the container image location if it is not known to the interchange"""
        if container_uuid not in self.containers:
            if container_uuid == 'RAW' or not container_uuid:
                self.containers[container_uuid] = 'RAW'
            else:
                try:
                    container = self.fxs.get_container(container_uuid, self.config.container_type)
                except Exception:
                    logger.exception("[FETCH_CONTAINER] Unable to resolve container location")
                    self.containers[container_uuid] = 'RAW'
                else:
                    logger.info("[FETCH_CONTAINER] Got container info: {}".format(container))
                    self.containers[container_uuid] = container.get('location', 'RAW')
        return self.containers[container_uuid]

    def get_total_tasks_outstanding(self):
        """ Get the outstanding tasks in total
        """
        outstanding = {}
        for task_type in self.pending_task_queue:
            outstanding[task_type] = outstanding.get(task_type, 0) + self.pending_task_queue[task_type].qsize()
        for manager in self._ready_manager_queue:
            for task_type in self._ready_manager_queue[manager]['tasks']:
                outstanding[task_type] = outstanding.get(task_type, 0) + len(self._ready_manager_queue[manager]['tasks'][task_type])
        return outstanding

    def get_total_live_workers(self):
        """ Get the total active workers
        """
        active = 0
        for manager in self._ready_manager_queue:
            if self._ready_manager_queue[manager]['active']:
                active += self._ready_manager_queue[manager]['max_worker_count']
        return active

    def get_outstanding_breakdown(self):
        """ Get outstanding breakdown per manager and in the interchange queues

        Returns
        -------
        List of status for online elements
        [ (element, tasks_pending, status) ... ]
        """

        pending_on_interchange = self.total_pending_task_count
        # Reporting pending on interchange is a deviation from Parsl
        reply = [('interchange', pending_on_interchange, True)]
        for manager in self._ready_manager_queue:
            resp = (manager.decode('utf-8'),
                    sum([len(tids) for tids in self._ready_manager_queue[manager]['tasks'].values()]),
                    self._ready_manager_queue[manager]['active'])
            reply.append(resp)
        return reply

    def _hold_block(self, block_id):
        """ Sends hold command to all managers which are in a specific block

        Parameters
        ----------
        block_id : str
             Block identifier of the block to be put on hold
        """
        for manager in self._ready_manager_queue:
            if self._ready_manager_queue[manager]['active'] and \
               self._ready_manager_queue[manager]['block_id'] == block_id:
                logger.debug("[HOLD_BLOCK]: Sending hold to manager: {}".format(manager))
                self.hold_manager(manager)

    def hold_manager(self, manager):
        """ Put manager on hold
        Parameters
        ----------

        manager : str
          Manager id to be put on hold while being killed
        """
        if manager in self._ready_manager_queue:
            self._ready_manager_queue[manager]['active'] = False

    def _status_report_loop(self, kill_event, status_report_queue: queue.Queue):
        logger.debug("[STATUS] Status reporting loop starting")

        while not kill_event.is_set():
            msg = EPStatusReport(
                self.endpoint_id,
                self.get_status_report(),
                self.task_status_deltas
            )
            logger.info("[STATUS] Sending status report to forwarder, and clearing task deltas.")
            status_report_queue.put(msg.pack())
            self.task_status_deltas.clear()
            time.sleep(self.heartbeat_period)

    def _command_server(self, kill_event):
        """ Command server to run async command to the interchange

        We want to be able to receive the following not yet implemented/updated commands:
         - OutstandingCount
         - ListManagers (get outstanding broken down by manager)
         - HoldWorker
         - Shutdown
        """
        logger.debug("[COMMAND] Command Server Starting")

        while not kill_event.is_set():
            try:
                # Wait for 1000 ms
                buffer = self.command_channel.get(timeout=1000)
                logger.debug(f"[COMMAND] Received command request {buffer}")
                command = Message.unpack(buffer)
                if command.type not in COMMAND_TYPES:
                    logger.error("Received incorrect message type on command channel")
                    self.command_channel.put(bytes())
                    continue

                if command.type is MessageType.HEARTBEAT_REQ:
                    logger.info("[COMMAND] Received synchonous HEARTBEAT_REQ from hub")
                    logger.info(f"[COMMAND] Replying with Heartbeat({self.endpoint_id})")
                    reply = Heartbeat(self.endpoint_id)

                logger.debug("[COMMAND] Reply: {}".format(reply))
                self.command_channel.put(reply.pack())

            except zmq.Again:
                logger.debug("[COMMAND] is alive")
                continue

    def stop(self):
        """Prepare the interchange for shutdown"""
        self._kill_event.set()

        self._task_puller_thread.join()
        self._command_thread.join()

    def start(self, poll_period=None):
        """ Start the Interchange

        Parameters:
        ----------
        poll_period : int
           poll_period in milliseconds
        """

        print("In start")
        """
        self.task_incoming.put('forwarder', b'hello from worker')
        for i in range(100):
            logger.info("Sending message")
            try:
                x= self.task_incoming.get()
                print("Got message from server : ", x)
            except:
                print("Sleeping")

           time.sleep(5)
        print("End debug")
        """
        logger.info("Incoming ports bound")

        if poll_period is None:
            poll_period = self.poll_period

        start = time.time()
        count = 0

        self._kill_event = threading.Event()
        self._status_request = threading.Event()
        self._task_puller_thread = threading.Thread(target=self.migrate_tasks_to_internal,
                                                    args=(self._kill_event, self._status_request, ))
        self._task_puller_thread.start()

        self._command_thread = threading.Thread(target=self._command_server,
                                                args=(self._kill_event, ))
        self._command_thread.start()

        status_report_queue = queue.Queue()
        self._status_report_thread = threading.Thread(target=self._status_report_loop,
                                                      args=(self._kill_event, status_report_queue))
        self._status_report_thread.start()

        try:
            logger.debug("Starting strategy.")
            self.strategy.start(self)
        except RuntimeError as e:
            # This is raised when re-registering an endpoint as strategy already exists
            logger.debug("Failed to start strategy.")
            logger.info(e)

        poller = zmq.Poller()
        # poller.register(self.task_incoming, zmq.POLLIN)
        poller.register(self.task_outgoing, zmq.POLLIN)
        poller.register(self.results_incoming, zmq.POLLIN)

        # These are managers which we should examine in an iteration
        # for scheduling a job (or maybe any other attention?).
        # Anything altering the state of the manager should add it
        # onto this list.
        interesting_managers = set()

        while not self._kill_event.is_set():
            self.socks = dict(poller.poll(timeout=poll_period))

            # Listen for requests for work
            if self.task_outgoing in self.socks and self.socks[self.task_outgoing] == zmq.POLLIN:
                logger.debug("[MAIN] starting task_outgoing section")
                message = self.task_outgoing.recv_multipart()
                manager = message[0]

                if manager not in self._ready_manager_queue:
                    reg_flag = False

                    try:
                        msg = json.loads(message[1].decode('utf-8'))
                        reg_flag = True
                    except Exception:
                        logger.warning("[MAIN] Got a non-json registration message from manager:{}".format(
                            manager))
                        logger.debug("[MAIN] Message :\n{}\n".format(message))

                    # By default we set up to ignore bad nodes/registration messages.
                    self._ready_manager_queue[manager] = {'last': time.time(),
                                                          'reg_time': time.time(),
                                                          'free_capacity': {'total_workers': 0},
                                                          'max_worker_count': 0,
                                                          'active': True,
                                                          'tasks': collections.defaultdict(set),
                                                          'total_tasks': 0}
                    if reg_flag is True:
                        interesting_managers.add(manager)
                        logger.info("[MAIN] Adding manager: {} to ready queue".format(manager))
                        self._ready_manager_queue[manager].update(msg)
                        logger.info("[MAIN] Registration info for manager {}: {}".format(manager, msg))

                        if (msg['python_v'].rsplit(".", 1)[0] != self.current_platform['python_v'].rsplit(".", 1)[0] or
                            msg['parsl_v'] != self.current_platform['parsl_v']):
                            logger.warn("[MAIN] Manager {} has incompatible version info with the interchange".format(manager))

                            if self.suppress_failure is False:
                                logger.debug("Setting kill event")
                                self._kill_event.set()
                                e = ManagerLost(manager)
                                result_package = {'task_id': -1,
                                                  'exception': self.serializer.serialize(e)}
                                pkl_package = pickle.dumps(result_package)
                                self.results_outgoing.put('forwarder', pkl_package)
                                logger.warning("[MAIN] Sent failure reports, unregistering manager")
                            else:
                                logger.debug("[MAIN] Suppressing shutdown due to version incompatibility")

                    else:
                        # Registration has failed.
                        if self.suppress_failure is False:
                            logger.debug("Setting kill event for bad manager")
                            self._kill_event.set()
                            e = BadRegistration(manager, critical=True)
                            result_package = {'task_id': -1,
                                              'exception': self.serializer.serialize(e)}
                            pkl_package = pickle.dumps(result_package)
                            self.results_outgoing.put('forwarder', pkl_package)
                        else:
                            logger.debug("[MAIN] Suppressing bad registration from manager:{}".format(
                                manager))

                else:
                    self._ready_manager_queue[manager]['last'] = time.time()
                    if message[1] == b'HEARTBEAT':
                        logger.debug("[MAIN] Manager {} sends heartbeat".format(manager))
                        self.task_outgoing.send_multipart([manager, b'', PKL_HEARTBEAT_CODE])
                    else:
                        manager_adv = pickle.loads(message[1])
                        logger.debug("[MAIN] Manager {} requested {}".format(manager, manager_adv))
                        self._ready_manager_queue[manager]['free_capacity'].update(manager_adv)
                        self._ready_manager_queue[manager]['free_capacity']['total_workers'] = sum(manager_adv.values())
                        interesting_managers.add(manager)

            # If we had received any requests, check if there are tasks that could be passed

            logger.debug("[MAIN] Managers count (total/interesting): {}/{}".format(
                len(self._ready_manager_queue),
                len(interesting_managers)))

            task_dispatch, dispatched_task = naive_interchange_task_dispatch(interesting_managers,
                                                                             self.pending_task_queue,
                                                                             self._ready_manager_queue,
                                                                             scheduler_mode=self.config.scheduler_mode)
            self.total_pending_task_count -= dispatched_task

            for manager in task_dispatch:
                tasks = task_dispatch[manager]
                if tasks:
                    logger.info("[MAIN] Sending task message {} to manager {}".format(tasks, manager))
                    self.task_outgoing.send_multipart([manager, b'', pickle.dumps(tasks)])
                    for task in tasks:
                        task_id = task.task_id
                        logger.debug(f"[MAIN] Task {task_id} is now WAITING_FOR_LAUNCH")
                        self.task_status_deltas[task_id] = TaskStatusCode.WAITING_FOR_LAUNCH

            # Receive any results and forward to client
            if self.results_incoming in self.socks and self.socks[self.results_incoming] == zmq.POLLIN:
                logger.debug("[MAIN] entering results_incoming section")
                manager, *b_messages = self.results_incoming.recv_multipart()
                if manager not in self._ready_manager_queue:
                    logger.warning("[MAIN] Received a result from a un-registered manager: {}".format(manager))
                else:
                    # We expect the batch of messages to be (optionally) a task status update message
                    # followed by 0 or more task results
                    try:
                        logger.debug("[MAIN] Trying to unpack ")
                        manager_report = Message.unpack(b_messages[0])
                        logger.info(f"[MAIN] Got manager status report: {manager_report.task_statuses}")
                        self.task_status_deltas.update(manager_report.task_statuses)
                        self.task_outgoing.send_multipart([manager, b'', PKL_HEARTBEAT_CODE])
                        b_messages = b_messages[1:]
                        self._ready_manager_queue[manager]['last'] = time.time()
                    except Exception:
                        pass
                    logger.info("[MAIN] Got {} result items in batch".format(len(b_messages)))
                    for b_message in b_messages:
                        r = pickle.loads(b_message)
                        logger.debug("[MAIN] Received result for task {} from {}".format(r['task_id'], manager))
                        logger.debug(f"[MAIN] Results : {r}")
                        task_type = self.containers[r['container_id']]
                        if r['task_id'] in self.task_status_deltas:
                            del self.task_status_deltas[r['task_id']]
                        self._ready_manager_queue[manager]['tasks'][task_type].remove(r['task_id'])
                        self.results_outgoing.put('forwarder', b_message)
                    self._ready_manager_queue[manager]['total_tasks'] -= len(b_messages)

                    # TODO: handle this with a Task message or something?
                    # previously used this; switched to mono-message, # self.results_outgoing.send_multipart(b_messages)

                    logger.debug("[MAIN] Current tasks: {}".format(self._ready_manager_queue[manager]['tasks']))
                logger.debug("[MAIN] leaving results_incoming section")

            # Send status reports from this main thread to avoid thread-safety on zmq sockets
            try:
                packed_status_report = status_report_queue.get(block=False)
                logger.debug(f"[MAIN] forwarding status report queue: {packed_status_report}")
                self.results_outgoing.put('forwarder', packed_status_report)
            except queue.Empty:
                pass

            # logger.debug("[MAIN] entering bad_managers section")
            bad_managers = [manager for manager in self._ready_manager_queue if
                            time.time() - self._ready_manager_queue[manager]['last'] > self.heartbeat_threshold]
            for manager in bad_managers:
                logger.debug("[MAIN] Last: {} Current: {}".format(self._ready_manager_queue[manager]['last'], time.time()))
                logger.warning("[MAIN] Too many heartbeats missed for manager {}".format(manager))
                e = ManagerLost(manager)
                for task_type in self._ready_manager_queue[manager]['tasks']:
                    for tid in self._ready_manager_queue[manager]['tasks'][task_type]:
                        result_package = {'task_id': tid, 'exception': self.serializer.serialize(e)}
                        pkl_package = pickle.dumps(result_package)
                        self.results_outgoing.send(pkl_package)
                logger.warning("[MAIN] Sent failure reports, unregistering manager")
                self._ready_manager_queue.pop(manager, 'None')
                if manager in interesting_managers:
                    interesting_managers.remove(manager)
            logger.debug("[MAIN] ending one main loop iteration")

            if self._status_request.is_set():
                logger.info("status request response")
                result_package = self.get_status_report()
                pkl_package = pickle.dumps(result_package)
                self.results_outgoing.send(pkl_package)
                logger.info("[MAIN] Sent info response")
                self._status_request.clear()

        delta = time.time() - start
        logger.info("Processed {} tasks in {} seconds".format(count, delta))
        logger.warning("Exiting")

    def get_status_report(self):
        """ Get utilization numbers
        """
        total_cores = 0
        total_mem = 0
        core_hrs = 0
        active_managers = 0
        free_capacity = 0
        outstanding_tasks = self.get_total_tasks_outstanding()
        pending_tasks = self.total_pending_task_count
        num_managers = len(self._ready_manager_queue)
        live_workers = self.get_total_live_workers()

        for manager in self._ready_manager_queue:
            total_cores += self._ready_manager_queue[manager]['cores']
            total_mem += self._ready_manager_queue[manager]['mem']
            active_dur = abs(time.time() - self._ready_manager_queue[manager]['reg_time'])
            core_hrs += (active_dur * total_cores) / 3600
            if self._ready_manager_queue[manager]['active']:
                active_managers += 1
            free_capacity += self._ready_manager_queue[manager]['free_capacity']['total_workers']

        result_package = {'task_id': -2,
                          'info': {'total_cores': total_cores,
                                   'total_mem': total_mem,
                                   'new_core_hrs': core_hrs - self.last_core_hr_counter,
                                   'total_core_hrs': round(core_hrs, 2),
                                   'managers': num_managers,
                                   'active_managers': active_managers,
                                   'total_workers': live_workers,
                                   'idle_workers': free_capacity,
                                   'pending_tasks': pending_tasks,
                                   'outstanding_tasks': outstanding_tasks,
                                   'worker_mode': self.config.worker_mode,
                                   'scheduler_mode': self.config.scheduler_mode,
                                   'scaling_enabled': self.config.scaling_enabled,
                                   'mem_per_worker': self.config.mem_per_worker,
                                   'cores_per_worker': self.config.cores_per_worker,
                                   'prefetch_capacity': self.config.prefetch_capacity,
                                   'max_blocks': self.config.provider.max_blocks,
                                   'min_blocks': self.config.provider.min_blocks,
                                   'max_workers_per_node': self.config.max_workers_per_node,
                                   'nodes_per_block': self.config.provider.nodes_per_block
        }}

        self.last_core_hr_counter = core_hrs
        return result_package

    def scale_out(self, blocks=1, task_type=None):
        """Scales out the number of blocks by "blocks"

        Raises:
             NotImplementedError
        """
        r = []
        for i in range(blocks):
            if self.config.provider:
                self._block_counter += 1
                external_block_id = str(self._block_counter)
                if not task_type and self.config.scheduler_mode == 'hard':
                    launch_cmd = self.launch_cmd.format(block_id=external_block_id, worker_type='RAW')
                else:
                    launch_cmd = self.launch_cmd.format(block_id=external_block_id, worker_type=task_type)
                if not task_type:
                    internal_block = self.config.provider.submit(launch_cmd, 1)
                else:
                    internal_block = self.config.provider.submit(launch_cmd, 1, task_type)
                logger.debug("Launched block {}->{}".format(external_block_id, internal_block))
                if not internal_block:
                    raise(ScalingFailed(self.provider.label,
                                        "Attempts to provision nodes via provider has failed"))
                self.blocks[external_block_id] = internal_block
                self.block_id_map[internal_block] = external_block_id
            else:
                logger.error("No execution provider available")
                r = None
        return r

    def scale_in(self, blocks=None, block_ids=[], task_type=None):
        """Scale in the number of active blocks by specified amount.

        Parameters
        ----------
        blocks : int
            # of blocks to terminate

        block_ids : [str.. ]
            List of external block ids to terminate
        """
        if task_type:
            logger.info("Scaling in blocks of specific task type {}. Let the provider decide which to kill".format(task_type))
            if self.config.scaling_enabled and self.config.provider:
                to_kill, r = self.config.provider.cancel(blocks, task_type)
                logger.info("Get the killed blocks: {}, and status: {}".format(to_kill, r))
                for job in to_kill:
                    logger.info("[scale_in] Getting the block_id map {} for job {}".format(self.block_id_map, job))
                    block_id = self.block_id_map[job]
                    logger.info("[scale_in] Holding block {}".format(block_id))
                    self._hold_block(block_id)
                    self.blocks.pop(block_id)
                return r

        if block_ids:
            block_ids_to_kill = block_ids
        else:
            block_ids_to_kill = list(self.blocks.keys())[:blocks]

        # Try a polite terminate
        # TODO : Missing logic to hold blocks
        for block_id in block_ids_to_kill:
            self._hold_block(block_id)

        # Now kill via provider
        to_kill = [self.blocks.pop(bid) for bid in block_ids_to_kill]

        if self.config.scaling_enabled and self.config.provider:
            r = self.config.provider.cancel(to_kill)

        return r

    def provider_status(self):
        """ Get status of all blocks from the provider
        """
        status = []
        if self.config.provider:
            logger.debug("[MAIN] Getting the status of {} blocks.".format(list(self.blocks.values())))
            status = self.config.provider.status(list(self.blocks.values()))
            logger.debug("[MAIN] The status is {}".format(status))

        return status


def start_file_logger(filename, name="interchange", level=logging.DEBUG, format_string=None):
    """Add a stream log handler.

    Parameters
    ---------

    filename: string
        Name of the file to write logs to. Required.
    name: string
        Logger name. Default="parsl.executors.interchange"
    level: logging.LEVEL
        Set the logging level. Default=logging.DEBUG
        - format_string (string): Set the format string
    format_string: string
        Format string to use.

    Returns
    -------
        None.
    """
    if format_string is None:
        format_string = "%(asctime)s.%(msecs)03d %(name)s:%(lineno)d [%(levelname)s]  %(message)s"

    global logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not len(logger.handlers):
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def starter(comm_q, *args, **kwargs):
    """Start the interchange process

    The executor is expected to call this function. The args, kwargs match that of the Interchange.__init__
    """
    # logger = multiprocessing.get_logger()
    ic = Interchange(*args, **kwargs)
    comm_q.put((ic.worker_task_port,
                ic.worker_result_port))
    ic.start()


def cli_run():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--client_address", required=True,
                        help="Client address")
    parser.add_argument("--client_ports", required=True,
                        help="client ports as a triple of outgoing,incoming,command")
    parser.add_argument("--worker_port_range",
                        help="Worker port range as a tuple")
    parser.add_argument("-l", "--logdir", default="./parsl_worker_logs",
                        help="Parsl worker log directory")
    parser.add_argument("-p", "--poll_period",
                        help="REQUIRED: poll period used for main thread")
    parser.add_argument("--worker_ports", default=None,
                        help="OPTIONAL, pair of workers ports to listen on, eg --worker_ports=50001,50005")
    parser.add_argument("--suppress_failure", action='store_true',
                        help="Enables suppression of failures")
    parser.add_argument("--endpoint_id", required=True,
                        help="Endpoint ID, used to identify the endpoint to the remote broker")
    parser.add_argument("--hb_threshold",
                        help="Heartbeat threshold in seconds")
    parser.add_argument("--config", default=None,
                        help="Configuration object that describes provisioning")
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Enables debug logging")

    print("Starting HTEX Intechange")
    args = parser.parse_args()

    optionals = {}
    optionals['suppress_failure'] = args.suppress_failure
    optionals['logdir'] = os.path.abspath(args.logdir)
    optionals['client_address'] = args.client_address
    optionals['client_ports'] = [int(i) for i in args.client_ports.split(',')]
    optionals['endpoint_id'] = args.endpoint_id

    # DEBUG ONLY : TODO: FIX
    if args.config is None:
        from funcx_endpoint.endpoint.utils.config import Config
        from parsl.providers import LocalProvider

        config = Config(
            worker_debug=True,
            scaling_enabled=True,
            provider=LocalProvider(
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
            ),
            max_workers_per_node=2,
            # funcx_service_address='https://api.funcx.org/v1'
            funcx_service_address='http://127.0.0.1:8080'
        )
        optionals['config'] = config
    else:
        optionals['config'] = args.config

    if args.debug:
        optionals['logging_level'] = logging.DEBUG
    if args.worker_ports:
        optionals['worker_ports'] = [int(i) for i in args.worker_ports.split(',')]
    if args.worker_port_range:
        optionals['worker_port_range'] = [int(i) for i in args.worker_port_range.split(',')]

    ic = Interchange(**optionals)
    ic.start()

    """
    with daemon.DaemonContext():
    """
