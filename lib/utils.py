import inspect
import json
import subprocess
import time
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, Dict

import mido
from loguru import logger
from protocol0.application.command.SerializableCommand import SerializableCommand
from protocol0.domain.shared.errors.Protocol0Error import Protocol0Error


def filename_datetime() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def unlink_if_exists(path: Path):
    if path.exists():
        try:
            path.unlink()
        except PermissionError as e:
            logger.error(e)


def copy_to_clipboard(data: str):
    subprocess.run("clip", universal_newlines=True, input=data)


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
            None,
        )
        if isinstance(cls, type):
            return cls
    return None


def log_string(string) -> str:
    return str(string).replace("<", "\\<")


def make_sysex_message_from_command(command: SerializableCommand) -> mido.Message:
    assert isinstance(command, SerializableCommand), (
        "expected SerializableCommand, got %s" % command
    )
    message = command.serialize()
    b = bytearray(message.encode())
    b.insert(0, 0xF0)
    b.append(0xF7)
    return mido.Message.from_bytes(b)


def make_script_command_from_sysex_message(message: mido.Message) -> Optional[SerializableCommand]:
    dict = make_dict_from_sysex_message(message)
    if dict is None:
        return None
    try:
        return SerializableCommand.un_serialize(json.dumps(dict))
    except (AssertionError, Protocol0Error):
        return None


def make_sysex_message_from_dict(data: Dict) -> mido.Message:
    assert isinstance(data, Dict)
    message = json.dumps(data, default=str)
    b = bytearray(message.encode())
    b.insert(0, 0xF0)
    b.append(0xF7)
    return mido.Message.from_bytes(b)


def make_dict_from_sysex_message(message: mido.Message) -> Optional[Dict]:
    if message.is_cc(121) or message.is_cc(123):
        # logger.debug("skipping cc 121 or 123")
        return None
    string = message.bin()[1:-1].decode("utf-8")  # type: str
    if not string.startswith("{"):
        return None
    try:
        return json.loads(string)
    except JSONDecodeError:
        logger.error(f"json decode error on string : {string}, message: {message}")
        return None
