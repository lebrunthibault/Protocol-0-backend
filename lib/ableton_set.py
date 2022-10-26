import re
from typing import List, Dict, Optional

from loguru import logger
from pydantic import BaseModel

from api.client.p0_script_api_client import p0_script_client_from_http, p0_script_client
from gui.celery import notification_window
from lib.ableton.ableton import is_ableton_focused
from lib.ableton.get_set import (
    _get_window_title_from_filename,
    get_recently_launched_set,
    get_launched_sets,
)
from lib.enum.NotificationEnum import NotificationEnum
from lib.window.window import get_focused_window_title
from protocol0.application.command.ActivateSetCommand import ActivateSetCommand
from protocol0.application.command.GetSetStateCommand import GetSetStateCommand


class AbletonSet(BaseModel):
    def __repr__(self):
        return f"AbletonSet('{self.title}')"

    def __str__(self):
        return self.__repr__()

    id: str
    active: bool
    title: Optional[str]  # computed only by the backend
    muted: bool
    drum_rack_visible: bool
    room_eq_enabled: bool


class AbletonSetManager:
    DEBUG = False

    @classmethod
    def register(cls, ableton_set: AbletonSet):
        ableton_set.title = ableton_set.title or _get_window_title_from_filename(
            get_recently_launched_set()
        )

        # cleaning here in case a closed set didn't notify
        launched_sets = get_launched_sets()
        for ss in cls.all():
            if next(filter(lambda s: ss.title in s, launched_sets), None) is None:  # type: ignore
                cls.remove(ss.id)

        # deduplicate on set title
        existing_set = cls.from_title(ableton_set.title)

        _ableton_set_registry[ableton_set.id] = ableton_set
        if cls.DEBUG:
            logger.info(f"registering set {ableton_set}, existing: {existing_set and existing_set.id}")

        if existing_set is not None and existing_set.id != ableton_set.id:
            cls.remove(existing_set.id)
        if existing_set is None:
            # it's an update
            cls.sync(active_set=ableton_set)

    @classmethod
    def remove(cls, id: str):
        if cls.DEBUG:
            logger.info(f"removing {id}")

        if id in _ableton_set_registry:
            del _ableton_set_registry[id]

    @classmethod
    def get(cls, id: str) -> AbletonSet:
        return _ableton_set_registry[id]

    @classmethod
    def active(cls) -> Optional[AbletonSet]:
        return next(filter(lambda s: s.active, cls.all()), None)  # type: ignore

    @classmethod
    def from_title(cls, title: str) -> Optional[AbletonSet]:
        return next(filter(lambda s: s.title == title, cls.all()), None)  # type: ignore

    @classmethod
    def all(cls) -> List[AbletonSet]:
        return list(_ableton_set_registry.values())

    @classmethod
    def sync(cls, active_set: AbletonSet = None) -> None:
        if active_set is None:
            p0_script_client().dispatch(GetSetStateCommand())

        active_set = active_set or get_focused_set()

        if active_set is None:
            notification_window.delay("No set focused", NotificationEnum.WARNING.value)
            return

        for ss in cls.all():
            ss.active = ss == active_set
            command = ActivateSetCommand(ss.active)
            command.set_id = ss.id
            p0_script_client_from_http().dispatch(command)

        if len(cls.all()) > 1:
            notification_window.delay(f"Activated '{active_set.title}'")
        else:
            notification_window.delay("Only one set launched")


# in-memory registry
_ableton_set_registry: Dict[str, AbletonSet] = {}


def get_focused_set() -> Optional[AbletonSet]:
    if not is_ableton_focused():
        return None

    title = get_focused_window_title()
    if AbletonSetManager.DEBUG:
        logger.info(f"focused_window_title: {title}")

    match = re.match("([^[*]*)\*?\s*(\[[^[]*])? - Ableton Live.*", title)

    if match is None:
        return None
    set_title = match.group(1).strip()

    return AbletonSetManager.from_title(set_title)
