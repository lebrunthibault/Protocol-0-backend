import glob
import os
import re
import time
from os.path import dirname

import keyboard  # noqa
from loguru import logger

from config import Config


def get_last_launched_set(excluded_keywords=("default", "master", "kontakt")) -> str:
    set_filenames = glob.glob(f"{Config.ABLETON_SET_DIRECTORY}\\*.als") + glob.glob(
        f"{Config.ABLETON_SET_DIRECTORY}\\tracks\\**\\*.als"
    )

    track_set_filenames = filter(
        lambda name: not any(excluded in name.lower() for excluded in excluded_keywords),
        set_filenames,
    )

    return max(track_set_filenames, key=os.path.getatime)


def get_recently_launched_set() -> str:
    set = get_last_launched_set(excluded_keywords=())
    atime = os.path.getatime(set)
    logger.info(f"Last launched set : {set} {round(time.time() - atime, 2)} seconds ago")

    # max 60 seconds to open up
    if time.time() - atime > 60:
        return Config.ABLETON_DEFAULT_SET

    return set


def get_kontakt_set() -> str:
    main_set = get_last_launched_set()

    set_folder = dirname(main_set)
    if set_folder != Config.ABLETON_SET_DIRECTORY:
        sets = glob.glob(f"{set_folder}\\*.als")
        kontakt_set = next(filter(lambda s: "kontakt" in s.lower(), sets), None)
        if kontakt_set is not None:
            return kontakt_set

    return Config.ABLETON_KONTAKT_SET


def get_window_title_from_filename(filename: str) -> str:
    # for matching against window title
    if filename == Config.ABLETON_DEFAULT_SET:
        return "Untitled"

    return re.search("([^\\\]*)\.als", filename).group(1)
