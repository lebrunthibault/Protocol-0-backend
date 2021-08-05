import asyncio

import asyncclick as click
from loguru import logger

from lib.window.terminal import clear_terminal
from scripts.abstract_cli import setup_cli
from sr.dictionary.dictionary_manager import DictionaryManager
from sr.speech_recognition.speech_recognition_main import recognize_speech
from sr.speech_recognition.speech_recognition_training_set_collector import collect_short_sound_recordings

setup_cli()


@click.group()
async def cli() -> None:
    clear_terminal()
    logger.info("launching speech cli command")


@cli.command(name="run")
async def command_run() -> None:
    recognize_speech()
    await asyncio.Future()  # make asyncio run forever


@cli.command(name="train")
@click.argument("target_word")
async def command_train(target_word: str) -> None:
    collect_short_sound_recordings(target_word=target_word)
    await asyncio.Future()  # make asyncio run forever


@cli.command(name="create_dict")
def command_create_dict() -> None:
    DictionaryManager().generate_from_results()


@cli.command(name="prepare")
def command_prepare() -> None:
    DictionaryManager().prepare_model_grammar()


if __name__ == "__main__":
    cli()
