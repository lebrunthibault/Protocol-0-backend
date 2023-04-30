import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from lib.ableton_set import AbletonSetManager
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
async def command_test() -> None:
    AbletonSetManager.set_title("Oblivion")


if __name__ == "__main__":
    cli()
