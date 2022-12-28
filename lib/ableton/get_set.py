import glob
import os
import re
from typing import List

from api.settings import Settings
from lib.window.find_window import get_windows_list

settings = Settings()


def get_ableton_windows() -> List[str]:
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


def _get_window_title_from_filename(filename: str) -> str:
    # for matching against window title
    if filename == settings.ableton_default_set:
        return "Untitled"

    return re.search("([^\\\]*)\.als", filename).group(1)
