import p0_backend_client

import make_path  # noqa
from api.midi_server.p0_backend_api_client import backend_client
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from config import Config
from lib.process import execute_process_in_new_window

from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    backend_client.test_duplication()
    execute_process_in_new_window(f"& \"{Config.ABLETON_CURRENT_SET}\"")


if __name__ == "__main__":
    cli()
