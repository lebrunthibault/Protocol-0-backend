import subprocess

from api.midi_app import start_midi_server
from commands.presets import sync_presets
from scripts.abstract_cli import cli
from scripts.commands.logoff import logoff
from scripts.commands.logon import logon


@cli.command(name="sync_presets")
def command_sync_presets() -> None:
    sync_presets()


@cli.command(name="midi_server")
def command_midi_server() -> None:
    start_midi_server()


@cli.command(name="http_server")
def command_http_server() -> None:
    subprocess.run(["uvicorn", "api.http_server.main:app", "--reload"])


@cli.command(name="celery")
def command_celery() -> None:
    subprocess.run(["celery", "-A", "gui", "worker", "-l", "info"])


@cli.command(name="logon")
def command_logon() -> None:
    logon()


@cli.command(name="logoff")
def command_logoff() -> None:
    logoff()


@cli.command(name="test")
def command_test() -> None:
    pass


if __name__ == "__main__":
    cli()
