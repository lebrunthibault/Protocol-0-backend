import glob
import os
import re
import time
from os.path import dirname
from typing import List, Optional

from api.settings import Settings
from gui.celery import notification_window
from lib.window.find_window import get_windows_list

settings = Settings()


def get_launched_sets() -> List[str]:
    set_infos = filter(lambda i: i["app_name"] == settings.ableton_process_name, get_windows_list())

    return [i["name"] for i in set_infos]


def get_last_launched_track_set(excluded_keywords=("default", "master", "midi")) -> str:
    """Last launched track"""
    set_filenames = glob.glob(f"{settings.ableton_set_directory}\\tracks\\**\\*.als")

    track_set_filenames = filter(
        lambda name: not any(excluded in name.lower() for excluded in excluded_keywords),
        set_filenames,
    )

    return max(track_set_filenames, key=os.path.getatime)


def get_recently_launched_set() -> str:
    set = get_last_launched_track_set(excluded_keywords=())
    atime = os.path.getatime(set)

    # max 60 seconds to open up
    if time.time() - atime > 60:
        return settings.ableton_default_set

    return set


def get_midi_set() -> Optional[str]:
    main_set = get_last_launched_track_set()

    set_folder = dirname(main_set)
    if set_folder != settings.ableton_set_directory:
        sets = glob.glob(f"{set_folder}\\*.als")
        midi_set = next(filter(lambda s: "midi" in s.lower(), sets), None)
        if midi_set is not None:
            return midi_set

    notification_window.delay(f"Couldn't find midi set in '{set_folder}'")

    return None


def _get_window_title_from_filename(filename: str) -> str:
    # for matching against window title
    if filename == settings.ableton_default_set:
        return "Untitled"

    return re.search("([^\\\]*)\.als", filename).group(1)
