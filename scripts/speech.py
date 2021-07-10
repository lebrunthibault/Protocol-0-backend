import click
from loguru import logger

from abstract_cli import setup_cli
from lib.window.terminal import clear_terminal
from sr.dictionary.DictionaryManager import DictionaryManager
from sr.speech_recognition.speech_recognition_main import SpeechRecognitionMain
from sr.speech_recognition.speech_recognition_trainer import SpeechRecognitionTrainer

setup_cli()


@click.group()
def cli() -> None:
    clear_terminal()
    logger.info("launching speech cli command")


@cli.command(name="run")
def command_run() -> None:
    SpeechRecognitionMain().recognize()


@cli.command(name="train")
@click.argument("target_word")
def command_train(target_word: str) -> None:
    SpeechRecognitionTrainer(target_word=target_word).recognize()


@cli.command(name="create_dict")
def command_create_dict() -> None:
    DictionaryManager().generate_from_results()


@cli.command(name="prepare")
def command_prepare() -> None:
    DictionaryManager().prepare_model_grammar()


if __name__ == "__main__":
    cli()
