import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from lib.process import execute_python_script_in_new_window
from scripts.abstract_cli import cli
from scripts.tail_protocol0_logs import settings


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


@cli.command(name="test")
def command_test() -> None:
    execute_python_script_in_new_window(
        f"{settings.project_directory}/scripts/tail_protocol0_logs.py"
    )


if __name__ == "__main__":
    cli()
