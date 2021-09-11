import ctypes

# import sys
# print(sys.version_info)
# sys.exit()
import asyncclick as click

from api.midi_app import start_midi_server
from api.p0_script_api_client import p0_script_api_client
from commands.reload_ableton import reload_ableton, save_set_as_template
from commands.sync_presets import sync_presets
from config import SystemConfig
from lib.process import execute_in_new_window
from lib.window.window import focus_window
from scripts.abstract_cli import cli
from scripts.commands.activate_rev2_editor import activate_rev2_editor
from scripts.commands.git_backup import backup_git_repos
from scripts.commands.search_set_gui import search_set_gui


@cli.command(name="reload_ableton")
def command_reload_ableton() -> None:
    reload_ableton()


@cli.command(name="focus_window")
@click.argument("name")
@click.argument("search_type", required=False)
def command_focus_window(name: str) -> None:
    focus_window(name)


@cli.command(name="search_set_gui")
def command_search_set_gui() -> None:
    search_set_gui()


@cli.command(name="sync_presets")
def command_sync_presets() -> None:
    sync_presets()


@cli.command(name="tail_logs")
@click.option('--raw', is_flag=True)
def command_tail_logs(raw: bool) -> None:
    args = ["--raw"] if raw else []
    execute_in_new_window(f"{SystemConfig.PROJECT_ROOT}/scripts/tail_protocol0_logs.py", *args)


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    save_set_as_template()


@cli.command(name="git_backup")
def command_git_backup() -> None:
    backup_git_repos()


@cli.command(name="midi")
def command_midi_server() -> None:
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.MIDI_SERVER_WINDOW_TITLE)
    start_midi_server()


@cli.command(name="ping")
def command_ping() -> None:
    p0_script_api_client.ping()


@cli.command(name="test")
def command_test() -> None:
    activate_rev2_editor()


if __name__ == "__main__":
    cli()
