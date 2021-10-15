import asyncclick as click

from api.midi_app import start_midi_server
from commands.sync_presets import sync_presets
from config import SystemConfig
from lib.ableton import reload_ableton, save_set_as_template
from lib.process import execute_in_new_window
from lib.window.window import focus_window
from scripts.abstract_cli import cli
from scripts.commands.activate_rev2_editor import activate_rev2_editor
from scripts.commands.git_backup import push_git_repos, pull_git_repos
from scripts.commands.logoff import logoff


@cli.command(name="reload_ableton")
def command_reload_ableton() -> None:
    reload_ableton()


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


@cli.command(name="save_set_as_template")
def command_save_set_as_template() -> None:
    save_set_as_template()


@cli.command(name="git_backup")
def command_push_git_repos() -> None:
    push_git_repos()


@cli.command(name="git_pull")
def command_pull_git_repos() -> None:
    pull_git_repos()


@cli.command(name="midi")
def command_midi_server() -> None:
    start_midi_server()


@cli.command(name="logoff")
def command_logoff() -> None:
    logoff()


@cli.command(name="test")
def command_test() -> None:
    activate_rev2_editor()


if __name__ == "__main__":
    cli()
