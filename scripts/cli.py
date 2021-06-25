import logging
import subprocess
import sys

from lib.custom_logging import configure_logging

configure_logging(filename="cli.log")

logger = logging.getLogger(__name__)

from typing import Optional

import click

from commands.reload_ableton import reload_ableton, save_set_as_template
from commands.search_set import search_set
from commands.sync_presets import sync_presets
from lib.window.find_window import SearchTypeEnum
from lib.window.window import focus_window


def exception_handler(exctype, value, tb):
    logger.error("Uncaught exception")
    logger.error(f"Type: {exctype}")
    logger.error(f"Value: {value}")
    if tb:
        format_exception = traceback.format_tb(tb)
        for line in format_exception:
            logger.error(repr(line))


sys.excepthook = exception_handler


@click.group()
def cli() -> None:
    pass


@cli.command(name="reload_ableton")
def command_reload_ableton() -> None:
    reload_ableton()


@cli.command(name="focus_window")
@click.argument("name")
@click.argument("search_type", required=False)
def command_focus_window(name: str, search_type: Optional[str]) -> None:
    search_type_enum = SearchTypeEnum.get_from_value(search_type, SearchTypeEnum.NAME)  # type: SearchTypeEnum
    focus_window(name, search_type_enum)


@cli.command(name="search_set")
def command_search_set() -> None:
    search_set()


@cli.command(name="sync_presets")
def command_sync_presets() -> None:
    sync_presets()


@cli.command(name="refresh_logs")
def command_refresh_logs() -> None:
    scripts_dir = "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\MIDI Remote Scripts\\a_protocol_0\\scripts"
    p = subprocess.Popen(["powershell.exe",
                          "invoke-expression",
                          "'cmd /c start powershell -Command { set-location \"%s\"; ./tailAbletonLogs.ps1 }'" % scripts_dir],
                         stdout=sys.stdout)
    p.communicate()


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    save_set_as_template()


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    save_set_as_template()


@cli.command(name="test")
def command_test() -> None:
    logger.info("test")


if __name__ == "__main__":
    cli()
