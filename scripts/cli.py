from loguru import logger

import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from lib.ableton.ableton import get_last_launched_set
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    logger.warning(get_last_launched_set())


if __name__ == "__main__":
    cli()
