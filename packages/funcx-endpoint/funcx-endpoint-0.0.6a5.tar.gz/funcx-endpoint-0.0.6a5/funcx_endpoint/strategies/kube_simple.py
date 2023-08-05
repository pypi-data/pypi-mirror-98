from funcx_endpoint.strategies.base import BaseStrategy
import math
import logging
import time

logger = logging.getLogger("interchange.strategy.KubeSimple")


class KubeSimpleStrategy(BaseStrategy):
    """ Implements the simple strategy for Kubernetes
    """

    def __init__(self, *args,
                 threshold=20,
                 interval=1,
                 max_idletime=60):
        """Initialize the flowcontrol object.

        We start the timer thread here

        Parameters
        ----------
        threshold:(int)
          Tasks after which the callback is triggered

        interval (int)
          seconds after which timer expires

        max_idletime: (int)
          maximum idle time(seconds) allowed for resources after which strategy will try to kill them.
          default: 60s

        """
        logger.info("KubeSimpleStrategy Initialized")
        super().__init__(*args, threshold=threshold, interval=interval)
        self.max_idletime = max_idletime
        self.executors_idle_since = {}

    def strategize(self, *args, **kwargs):
        try:
            self._strategize(*args, **kwargs)
        except Exception as e:
            logger.exception("Caught error in strategize : {}".format(e))
            pass

    def _strategize(self, *args, **kwargs):
        max_pods = self.interchange.config.provider.max_blocks
        min_pods = self.interchange.config.provider.min_blocks

        # Kubernetes provider only supports one manager in a pod
        managers_per_pod = 1

        workers_per_pod = self.interchange.config.max_workers_per_node
        if workers_per_pod == float('inf'):
            workers_per_pod = 1

        parallelism = self.interchange.config.provider.parallelism

        active_tasks = self.interchange.get_total_tasks_outstanding()
        logger.debug(f"Pending tasks : {active_tasks}")

        status = self.interchange.provider_status()
        logger.debug(f"Provider status : {status}")

        for task_type in active_tasks.keys():
            active_pods = status.get(task_type, 0)
            active_slots = active_pods * workers_per_pod * managers_per_pod
            active_tasks = active_tasks[task_type]

            logger.debug(
                'Endpoint has {} active tasks of {}, {} active blocks, {} connected workers for {}'.format(
                    active_tasks, task_type, active_pods,
                    self.interchange.get_total_live_workers(), task_type))

            # Reset the idle time if we are currently running tasks
            if active_tasks > 0:
                self.executors_idle_since[task_type] = None

            # Scale down only if there are no active tasks to avoid having to find which
            # workers are unoccupied
            if active_tasks == 0 and active_pods > min_pods:
                # We want to make sure that max_idletime is reached before killing off resources
                if not self.executors_idle_since[task_type]:
                    logger.debug(
                        "Endpoint has 0 active tasks of task type {}; starting kill timer (if idle time exceeds {}s, resources will be removed)".
                        format(task_type, self.max_idletime))
                    self.executors_idle_since[task_type] = time.time()

                # If we have resources idle for the max duration we have to scale_in now.
                if (time.time() - self.executors_idle_since[task_type]) > self.max_idletime:
                    logger.info(
                        "Idle time has reached {}s; removing resources of task type {}".format(
                            self.max_idletime, task_type)
                    )
                    self.interchange.scale_in(active_pods - min_pods, task_type=task_type)
            # More tasks than the available slots.
            elif active_tasks > 0 and (float(active_slots) / active_tasks) < parallelism:
                if active_pods < max_pods:
                    excess = math.ceil((active_tasks * parallelism) - active_slots)
                    excess_blocks = math.ceil(float(excess) / (workers_per_pod * managers_per_pod))
                    excess_blocks = min(excess_blocks, max_pods - active_pods)
                    logger.info("Requesting {} more blocks".format(excess_blocks))
                    self.interchange.scale_out(excess_blocks, task_type=task_type)
            # Immediatly scale if we are stuck with zero pods and work to do
            elif active_slots == 0 and active_tasks > 0:
                logger.info("Requesting single pod")
                self.interchange.scale_out(1, task_type=task_type)
