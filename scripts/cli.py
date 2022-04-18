import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from gui.celery import notification_window

from lib.enum.NotificationEnum import NotificationEnum
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    notification_window.delay("Saving the drum rack", NotificationEnum.WARNING.value)


if __name__ == "__main__":
    cli()
