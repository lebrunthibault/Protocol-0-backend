import asyncclick as click
from loguru import logger

from lib.window.terminal import clear_terminal
from scripts.abstract_cli import setup_cli
from sr.audio.recorder import _get_short_sounds_observable
from sr.audio.source.microphone import Microphone
from sr.dictionary.dictionary_manager import DictionaryManager
from sr.speech_recognition.speech_recognition_training_set_collector import SpeechRecognitionTrainingSetCollector

setup_cli()


@click.group()
def cli() -> None:
    clear_terminal()
    logger.info("launching speech cli command")


@cli.command(name="run")
async def command_run() -> None:
    await _get_short_sounds_observable(source=Microphone())
    # await SpeechRecognitionMain.recognize()


@cli.command(name="train")
@click.argument("target_word")
def command_train(target_word: str) -> None:
    SpeechRecognitionTrainingSetCollector.collect(target_word=target_word)


@cli.command(name="create_dict")
def command_create_dict() -> None:
    DictionaryManager().generate_from_results()


@cli.command(name="prepare")
def command_prepare() -> None:
    DictionaryManager().prepare_model_grammar()


if __name__ == "__main__":
    cli()
    print("after")
    loop = asyncio.get_event_loop()
    loop.run_forever()
