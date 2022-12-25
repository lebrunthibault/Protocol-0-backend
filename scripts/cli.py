from PIL import ImageGrab

import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
async def command_test() -> None:
    im2 = ImageGrab.grab(bbox=None)
    from loguru import logger
    logger.success(im2)


if __name__ == "__main__":
    cli()
