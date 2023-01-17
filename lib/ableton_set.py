import glob
import os.path
import re
import time
from os.path import basename, dirname
from typing import List, Dict, Optional

from loguru import logger
from pydantic import BaseModel

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from gui.celery import notification_window
from lib.ableton.ableton import is_ableton_focused
from lib.ableton.get_set import (
    get_ableton_windows,
    get_last_launched_track_set,
    _get_window_title_from_filename,
)
from lib.enum.notification_enum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.timer import start_timer
from lib.window.window import get_focused_window_title
from protocol0.application.command.ShowMessageCommand import ShowMessageCommand

settings = Settings()


class AbletonSet(BaseModel):
    def __repr__(self):
        return f"AbletonSet('{self.title}')"

    def __str__(self):
        return self.__repr__()

    id: str
    path: Optional[str]  # computed only by the backend
    title: Optional[str]  # computed only by the backend
    muted: bool
    current_track_name: str
    drum_rack_visible: bool
    room_eq_enabled: bool

    @property
    def is_untitled(self):
        return self.title is None
        # return self.title is None or self.title == "Untitled"

    @property
    def tracks_folder(self):
        assert self.path is not None, "current set is Untitled"
        return f"{dirname(self.path)}\\tracks"

    @classmethod
    def all_tracks_folder(cls) -> List[str]:
        return next(os.walk(f"{settings.ableton_set_directory}\\tracks"))[1]

    @property
    def temp_track_folder(self) -> str:
        return f"{settings.ableton_set_directory}\\tracks"

    @property
    def saved_temp_track(self) -> Optional[str]:
        return next(iter(glob.glob(f"{self.temp_track_folder}\\*.als")), None)

    @property
    def is_current_track_saved(self) -> bool:
        saved_track = self.saved_temp_track
        if saved_track is None:
            return False

        saved_track_name = basename(saved_track).replace(".als", "")

        assert saved_track_name == self.current_track_name, "track saved mismatch"
        assert time.time() - os.path.getmtime(saved_track) <= 2, "track not saved recently"

        return True


class AbletonSetManager:
    DEBUG = False
    LAST_SET_OPENED_AT: Optional[float] = None

    @classmethod
    async def register(cls, ableton_set: AbletonSet) -> bool:
        launched_sets = get_ableton_windows()

        is_untitled_set = len(launched_sets) == 1 and "Untitled" in launched_sets[0]
        if ableton_set.is_untitled:
            if is_untitled_set:
                ableton_set.path = settings.ableton_test_set_path
                ableton_set.title = "Toto"
            else:
                ableton_set.path = get_last_launched_track_set()
                ableton_set.title = _get_window_title_from_filename(ableton_set.path)

        # cleaning here in case a closed set didn't notify
        for ss in cls.all():
            if next(filter(lambda s: ss.title in s, launched_sets), None) is None:  # type: ignore
                await cls.remove(ss.id)

        # deduplicate on set title
        existing_set = cls.from_title(str(ableton_set.title))

        _ableton_set_registry[ableton_set.id] = ableton_set
        if cls.DEBUG or existing_set is None:
            logger.info(f"registering set {ableton_set}, existing: {existing_set is not None}")

        if existing_set is not None and existing_set.id != ableton_set.id:
            await cls.remove(existing_set.id)
        if existing_set is None:
            # it's an update
            await cls.sync(active_set=ableton_set)

        if cls.LAST_SET_OPENED_AT is not None:
            startup_duration = time.time() - cls.LAST_SET_OPENED_AT
            logger.info(f"took {startup_duration:.2f}")
            command = ShowMessageCommand(f"Startup took {startup_duration:.2f}s")
            start_timer(1, lambda: p0_script_client().dispatch(command))

            cls.LAST_SET_OPENED_AT = None

        return existing_set is None or existing_set.id != ableton_set.id

    @classmethod
    async def remove(cls, id: str):
        if cls.DEBUG:
            logger.info(f"removing {id}")

        if id in _ableton_set_registry:
            del _ableton_set_registry[id]

            # pass the active state to another set
            other_set = next(iter(cls.all()), None)
            if other_set is not None:
                await cls.sync(other_set)

    @classmethod
    def get(cls, id: str) -> AbletonSet:
        return _ableton_set_registry[id]

    @classmethod
    def active(cls) -> Optional[AbletonSet]:
        # take the first set
        active_set = next(iter(cls.all()), None)  # type: ignore

        if active_set is None:
            raise Protocol0Error("no active set")

        return active_set

    @classmethod
    def from_title(cls, title: str) -> Optional[AbletonSet]:
        return next(filter(lambda s: s.title == title, cls.all()), None)  # type: ignore

    @classmethod
    def all(cls) -> List[AbletonSet]:
        return list(_ableton_set_registry.values())

    @classmethod
    def clear(cls):
        for set in cls.all():
            cls.remove(set.id)

    @classmethod
    async def sync(cls, active_set: AbletonSet = None) -> None:
        active_set = active_set or get_focused_set()

        if active_set is None:
            notification_window.delay("No set focused", NotificationEnum.WARNING.value)
            return

        from api.http_server.ws import ws_manager

        await ws_manager.broadcast_server_state()


# in-memory registry
_ableton_set_registry: Dict[str, AbletonSet] = {}


def get_focused_set_title() -> Optional[str]:
    if not is_ableton_focused():
        return None

    title = get_focused_window_title()

    match = re.match("([^[*]*)\*?\s*(\[[^[]*])? - Ableton Live.*", title)

    if match is None:
        return None

    return match.group(1).strip()


def get_focused_set() -> Optional[AbletonSet]:
    set_title = get_focused_set_title()
    if set_title is None:
        return None

    return AbletonSetManager.from_title(set_title)
