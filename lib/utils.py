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
