import os
from os.path import dirname

from loguru import logger

import make_path  # noqa
from lib.ableton.get_set import get_last_launched_set

if __name__ == "__main__":
    folder = dirname(get_last_launched_set())
    logger.info(f"Opening {folder}")
    os.startfile(folder)
