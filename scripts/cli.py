import subprocess
import sys

import click
from loguru import logger

from abstract_cli import setup_cli
from api.p0_script_api_client import p0_script_api_client
from commands.reload_ableton import reload_ableton, save_set_as_template
from commands.sync_presets import sync_presets
from config import PROJECT_ROOT
from lib.window.terminal import clear_terminal
from lib.window.window import focus_window
from scripts.commands.git_backup import backup_git_repos
from scripts.commands.search_set_gui import search_set_gui

setup_cli()


@click.group()
def cli() -> None:
    clear_terminal()
    logger.info("launching cli command")


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


@cli.command(name="refresh_logs")
def command_refresh_logs() -> None:
    cwd = f"{PROJECT_ROOT}/scripts"
    p = subprocess.Popen(["powershell.exe",
                          "invoke-expression",
                          "'cmd /c start powershell -Command { set-location \"%s\"; py ./tail_protocol0_logs.py }'" % cwd],
                         stdout=sys.stdout)
    p.communicate()


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    save_set_as_template()


@cli.command(name="git_backup")
def command_git_backup() -> None:
    backup_git_repos()


@cli.command(name="search_set")
@click.argument("search")
def command_search_set(search: str) -> None:
    p0_script_api_client.search_track(search=search)
    logger.info("test")


@cli.command(name="test")
def command_test() -> None:
    logger.info("test")


if __name__ == "__main__":
    cli()
