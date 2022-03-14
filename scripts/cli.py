import requests

from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from config import Config
from lib.git import push_git_repos
from scripts.abstract_cli import cli
from scripts.commands.logoff import logoff
from scripts.commands.logon import logon


@cli.command(name="logon")
def command_logon() -> None:
    logon()


@cli.command(name="logoff")
def command_logoff() -> None:
    logoff()


@cli.command(name="git_backup")
def command_git_backup() -> None:
    push_git_repos()


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    try:
        r = requests.get(f"{Config.HTTP_API_URL}/")
    except requests.exceptions.ConnectionError:
        print("error")


if __name__ == "__main__":
    cli()
