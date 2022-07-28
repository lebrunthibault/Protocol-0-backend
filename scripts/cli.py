import os
import subprocess

from loguru import logger

import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs

from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    with open(os.path.devnull, "w+") as null:
        try:
            release = (
                subprocess.Popen(
                    ["git", "rev-parse", "HEAD"],
                    stdout=subprocess.PIPE,
                    stderr=null,
                    stdin=null,
                )
                .communicate()[0]
                .strip()
                .decode("utf-8")
            )
        except (OSError, IOError):
            pass

    logger.info(release)


if __name__ == "__main__":
    cli()
