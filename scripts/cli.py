import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from gui.celery import select_window
from lib.enum.ColorEnum import ColorEnum

from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    select_window.delay("hello", ["a", "b"], True, ColorEnum.INFO.value)


if __name__ == "__main__":
    cli()
