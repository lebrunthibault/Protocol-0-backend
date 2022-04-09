from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    pass


if __name__ == "__main__":
    cli()
