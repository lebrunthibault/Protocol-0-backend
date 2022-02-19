import time

import asyncclick as click

from api.midi_app import start_midi_server
from api.p0_system_api_client import system_client
from commands.presets import sync_presets
from config import SystemConfig
from lib.ableton import clear_arrangement
from lib.process import execute_in_new_window
from message_queue.celery import notification
from scripts.abstract_cli import cli
from scripts.commands.activate_rev2_editor import activate_rev2_editor
from scripts.commands.git_backup import push_git_repos, pull_git_repos
from scripts.commands.logoff import logoff
from scripts.commands.logon import logon
from sdk_generation.generate_openapi_specs import generate_openapi_specs


@cli.command(name="reload_ableton")
def command_reload_ableton() -> None:
    system_client.reload_ableton()


@cli.command(name="sync_presets")
def command_sync_presets() -> None:
    sync_presets()


@cli.command(name="tail_logs")
@click.option('--raw', is_flag=True)
def command_tail_logs(raw: bool) -> None:
    args = ["--raw"] if raw else []
    execute_in_new_window(f"{SystemConfig.PROJECT_ROOT}/scripts/tail_protocol0_logs.py", *args)


@cli.command(name="clear_logs")
def command_clear_logs() -> None:
    system_client.clear_logs()


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    system_client.save_set_as_template()


@cli.command(name="clear_arrangement")
def command_clear_arrangement() -> None:
    clear_arrangement()


@cli.command(name="git_backup")
def command_push_git_repos() -> None:
    push_git_repos()


@cli.command(name="git_pull")
def command_pull_git_repos() -> None:
    pull_git_repos()


@cli.command(name="midi")
def command_midi_server() -> None:
    start_midi_server()


@cli.command(name="logon")
def command_logon() -> None:
    logon()


@cli.command(name="logoff")
def command_logoff() -> None:
    logoff()


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    notification.delay(f"{time.time()}" * int(time.time() % 10))


if __name__ == "__main__":
    cli()
