import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from lib.ableton.interface.explorer import sort_by_name
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
async def command_test() -> None:
    from loguru import logger

    logger.success(sort_by_name(["Bass Support", "Bass"]))


if __name__ == "__main__":
    cli()
