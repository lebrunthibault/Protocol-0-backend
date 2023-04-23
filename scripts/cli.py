import make_path  # noqa
from protocol0.application.command.MidiNoteCommand import MidiNoteCommand
from api.client.p0_script_api_client import p0_script_client
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
async def command_test() -> None:
    return


if __name__ == "__main__":
    cli()
