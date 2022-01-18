from time import sleep

import asyncclick as click

from api.midi_app import start_midi_server, call_system_method
from api.routes import Routes
from commands.presets import sync_presets
from config import SystemConfig
from gui.window.notification.notification_factory import NotificationFactory
from gui.window.prompt.prompt_factory import PromptFactory
from gui.window.select.select_factory import SelectFactory
from lib.ableton import save_set_as_template, clear_arrangement
from lib.ableton_set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.enum.NotificationEnum import NotificationEnum
from lib.process import execute_in_new_window
from lib.window.window import focus_window
from scripts.abstract_cli import cli
from scripts.commands.git_backup import push_git_repos, pull_git_repos
from scripts.commands.logoff import logoff
from scripts.commands.logon import logon


@cli.command(name="reload_ableton")
def command_reload_ableton() -> None:
    call_system_method(AbletonSetProfiler.start_profiling_single_measurement)


@cli.command(name="focus_window")
@click.argument("name")
@click.argument("search_type", required=False)
def command_focus_window(name: str) -> None:
    focus_window(name)


@cli.command(name="sync_presets")
def command_sync_presets() -> None:
    sync_presets()


@cli.command(name="tail_logs")
@click.option('--raw', is_flag=True)
def command_tail_logs(raw: bool) -> None:
    args = ["--raw"] if raw else []
    execute_in_new_window(f"{SystemConfig.PROJECT_ROOT}/scripts/tail_protocol0_logs.py", *args)


@cli.command(name="clear_logs")
def command_tail_logs() -> None:
    call_system_method(Routes.clear_logs)


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    call_system_method(save_set_as_template)


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


@cli.command(name="test")
def command_test() -> None:
    # Routes.test()
    SelectFactory.createWindow(message="so ?", options=["toto", "titi", "tutu"], vertical=False).display()
    # PromptFactory.createWindow(message="so ?").display()
    # NotificationFactory.createWindow(message="hello\n agina\nagain", notification_enum=NotificationEnum.ERROR).display()
    sleep(10)


if __name__ == "__main__":
    cli()
