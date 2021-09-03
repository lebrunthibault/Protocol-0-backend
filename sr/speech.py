import asyncio

from scripts.abstract_cli import cli
from sr.recognizer.grammar_generation import prepare_model_grammar


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
