import asyncio

import asyncclick as click
from loguru import logger

from lib.window.terminal import clear_terminal
from scripts.abstract_cli import setup_cli
from sr.recognizer.grammar_generation import prepare_model_grammar


@click.group()
async def cli() -> None:
    setup_cli()
    clear_terminal()
    logger.info("launching speech cli command")


@cli.command(name="run")
async def command_run() -> None:
    from sr.speech_recognition.speech_recognition_main import recognize_speech
    recognize_speech()
    await asyncio.Future()  # make asyncio run forever


@cli.command(name="prepare")
def command_prepare() -> None:
    prepare_model_grammar()


if __name__ == "__main__":
    cli()
