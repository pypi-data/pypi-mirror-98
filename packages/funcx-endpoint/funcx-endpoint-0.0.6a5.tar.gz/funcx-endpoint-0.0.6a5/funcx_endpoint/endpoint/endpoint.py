import glob
from importlib.machinery import SourceFileLoader
import json
import logging
import os
import pathlib
import random
import shutil
import signal
import sys
import time
import uuid
from string import Template

import daemon
import daemon.pidfile
import psutil
import requests
import texttable as tt
import typer
from retry import retry

import funcx
import zmq

from funcx.utils.errors import *
from funcx_endpoint.endpoint import default_config as endpoint_default_config
from funcx_endpoint.executors.high_throughput import global_config as funcx_default_config
from funcx_endpoint.endpoint.interchange import EndpointInterchange
from funcx_endpoint.endpoint.endpoint_manager import EndpointManager
from funcx.sdk.client import FuncXClient

app = typer.Typer()


def version_callback(value):
    if value:
        import funcx_endpoint
        typer.echo("FuncX endpoint version: {}".format(funcx_endpoint.__version__))
        raise typer.Exit()


def complete_endpoint_name():
    config_files = glob.glob('{}/*/config.py'.format(manager.funcx_dir))
    for config_file in config_files:
        yield os.path.basename(os.path.dirname(config_file))


@app.command(name="configure", help="Configure an endpoint")
def configure_endpoint(
        name: str = typer.Argument("default", help="endpoint name", autocompletion=complete_endpoint_name),
        endpoint_config: str = typer.Option(None, "--endpoint-config", help="endpoint config file")
):
    """Configure an endpoint

    Drops a config.py template into the funcx configs directory.
    The template usually goes to ~/.funcx/<ENDPOINT_NAME>/config.py
    """
    manager.configure_endpoint(name, endpoint_config)


@app.command(name="start", help="Start an endpoint by name")
def start_endpoint(
        name: str = typer.Argument("default", autocompletion=complete_endpoint_name),
        endpoint_uuid: str = typer.Option(None, help="The UUID for the endpoint to register with")
):
    """Start an endpoint

    This function will do:
    1. Connect to the broker service, and register itself
    2. Get connection info from broker service
    3. Start the interchange as a daemon


    |                      Broker service       |
    |               -----2----> Forwarder       |
    |    /register <-----3----+   ^             |
    +-----^-----------------------+-------------+
          |     |                 |
          1     4                 6
          |     v                 |
    +-----+-----+-----+           v
    |      Start      |---5---> EndpointInterchange
    |     Endpoint    |         daemon
    +-----------------+

    Parameters
    ----------
    name : str
    endpoint_uuid : str
    """
    endpoint_dir = os.path.join(manager.funcx_dir, name)
    endpoint_config = SourceFileLoader('config',
                                       os.path.join(endpoint_dir, manager.funcx_config_file_name)).load_module()
    manager.start_endpoint(name, endpoint_uuid, endpoint_config)


@app.command(name="stop")
def stop_endpoint(name: str = typer.Argument("default", autocompletion=complete_endpoint_name)):
    """ Stops an endpoint using the pidfile

    """

    manager.stop_endpoint(name)


@app.command(name="restart")
def restart_endpoint(name: str = typer.Argument("default", autocompletion=complete_endpoint_name)):
    """Restarts an endpoint"""
    manager.stop_endpoint(name)
    manager.start_endpoint(name)


@app.command(name="list")
def list_endpoints():
    """ List all available endpoints
    """
    manager.list_endpoints()


@app.command(name="delete")
def delete_endpoint(
        name: str = typer.Argument(..., autocompletion=complete_endpoint_name),
        autoconfirm: bool = typer.Option(False, "-y", help="Do not ask for confirmation to delete.")
):
    """Deletes an endpoint and its config."""
    if not autoconfirm:
        typer.confirm(f"Are you sure you want to delete the endpoint <{name}>?", abort=True)

    manager.delete_endpoint(name)


@app.callback()
def main(
        ctx: typer.Context,
        _: bool = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True),
        debug: bool = typer.Option(False, "--debug", "-d"),
        config_dir: str = typer.Option('{}/.funcx'.format(pathlib.Path.home()), "--config_dir", "-c", help="override default config dir")
):
    # Note: no docstring here; the docstring for @app.callback is used as a help message for overall app.
    # Sets up global variables in the State wrapper (debug flag, config dir, default config file).
    # For commands other than `init`, we ensure the existence of the config directory and file.

    funcx.set_stream_logger(level=logging.DEBUG if debug else logging.INFO)
    logger = logging.getLogger('funcx')
    logger.debug("Command: {}".format(ctx.invoked_subcommand))

    global manager
    manager = EndpointManager(logger)

    # Set global state variables, to avoid passing them around as arguments all the time
    manager.DEBUG = debug
    manager.funcx_dir = config_dir
    manager.funcx_config_file = os.path.join(manager.funcx_dir, manager.funcx_config_file_name)

    # Otherwise, we ensure that configs exist
    if not os.path.exists(manager.funcx_config_file):
        manager.logger.info(f"No existing configuration found at {manager.funcx_config_file}. Initializing...")
        manager.init_endpoint()

    manager.logger.debug("Loading config files from {}".format(manager.funcx_dir))

    funcx_config = SourceFileLoader('global_config', manager.funcx_config_file).load_module()
    manager.funcx_config = funcx_config.global_options


def cli_run():
    """Entry point for setuptools to point to"""
    app()


if __name__ == '__main__':
    app()
