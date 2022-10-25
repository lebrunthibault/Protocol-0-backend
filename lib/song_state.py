from typing import List, Dict, Optional

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
from protocol0.application.command.EnableScriptCommand import EnableScriptCommand
from protocol0.application.command.GetSongStateCommand import GetSongStateCommand


class SongState(BaseModel):
    def __repr__(self):
        return f"SongState('{self.title}')"

    id: str
    enabled: bool
    title: Optional[str]  # computed only by the backend
    muted: bool
    drum_rack_visible: bool
    room_eq_enabled: bool


class SongStateManager:
    @classmethod
    def register(cls, song_state: SongState):
        song_state.title = song_state.title or _get_window_title_from_filename(
            get_recently_launched_set()
        )

        # cleaning here in case a closed set didn't notify
        launched_sets = get_launched_sets()
        for ss in cls.all():
            if next(filter(lambda s: ss.title in s, launched_sets), None) is None:  # type: ignore
                cls.remove(ss.id)

        # deduplicate on set title
        existing_song_state = cls.from_title(song_state.title)
        if existing_song_state is not None:
            cls.remove(existing_song_state.id)

        _song_state_registry[song_state.id] = song_state

    @classmethod
    def remove(cls, id: str):
        if id in _song_state_registry:
            del _song_state_registry[id]

    @classmethod
    def get(cls, id) -> SongState:
        return _song_state_registry[id]

    @classmethod
    def from_title(cls, title: str) -> Optional[SongState]:
        return next(filter(lambda s: s.title == title, cls.all()), None)  # type: ignore

    @classmethod
    def all(cls) -> List[SongState]:
        return list(_song_state_registry.values())

    @classmethod
    def sync(cls) -> None:
        focused_set = get_focused_set()

        if focused_set is None:
            notification_window.delay("No set focused", NotificationEnum.WARNING.value)
            return

        p0_script_client().dispatch(GetSongStateCommand())

        for ss in cls.all():
            command = EnableScriptCommand(ss == focused_set)
            command.set_id = ss.id
            p0_script_client_from_http().dispatch(command)

        notification_window.delay(f"Activated '{focused_set.title}'")


_song_state_registry: Dict[str, SongState] = {}


def get_focused_set() -> Optional[SongState]:
    if not is_ableton_focused():
        return None

    title = get_focused_window_title()
    if "*" in title:
        set_title = title.split("*")[0]
    else:
        set_title = title.split(" - Ableton Live")[0]

    return SongStateManager.from_title(set_title)
