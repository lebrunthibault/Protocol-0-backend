import subprocess
import sys
import time
from typing import Optional

import click
from loguru import logger

from abstract_cli import setup_cli
from commands.reload_ableton import reload_ableton, save_set_as_template
from commands.sync_presets import sync_presets
from lib.window.find_window import SearchTypeEnum
from lib.window.terminal import clear_terminal
from lib.window.window import focus_window
from scripts.commands.git_backups import backup_git_repos
from scripts.commands.search_set_gui import search_set_gui
from sr.speech_recognition.speech_recognition_main import SpeechRecognitionMain

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
def command_focus_window(name: str, search_type: Optional[str]) -> None:
    search_type_enum = SearchTypeEnum.get_from_value(search_type, SearchTypeEnum.NAME)  # type: SearchTypeEnum
    focus_window(name, search_type_enum)


@cli.command(name="search_set_gui")
def command_search_set_gui() -> None:
    search_set_gui()


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


@cli.command(name="test_toast")
def command_test_toast() -> None:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast("Sample Notification", "Python is awesome!!!", duration=0.5)
    while toaster.notification_active(): time.sleep(0.1)


@cli.command(name="speech")
def command_speech() -> None:
    SpeechRecognitionMain().recognize()


@cli.command(name="git_backup")
def command_git_backup() -> None:
    backup_git_repos()


@cli.command(name="test")
def command_test() -> None:
    logger.info("test")


if __name__ == "__main__":
    cli()
