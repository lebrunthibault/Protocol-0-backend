import requests

import make_path  # noqa
from api.midi_server.sdk_generation.generate_openapi_specs import generate_openapi_specs
from api.settings import Settings
from scripts.abstract_cli import cli


@cli.command(name="generate_openapi_specs")
def command_generate_openapi_specs() -> None:
    generate_openapi_specs()


def update_set_title():
    requests.put(f"{Settings().http_api_url}/set", params={"title": "Oblivion"})


@cli.command(name="test")
async def command_test() -> None:
    pass


if __name__ == "__main__":
    cli()
