import inspect
import subprocess
import time
from pathlib import Path

from loguru import logger


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
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return None
