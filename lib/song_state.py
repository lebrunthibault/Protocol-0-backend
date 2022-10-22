from typing import List, Dict, Optional

from pydantic import BaseModel

from lib.ableton.ableton import is_ableton_focused
from lib.ableton.get_set import (
    get_window_title_from_filename,
    get_recently_launched_set,
    get_launched_sets,
)
from lib.window.window import get_focused_window_title


class SongState(BaseModel):
    def __repr__(self):
        return f"SongState('{self.title}')"

    id: str
    title: Optional[str]  # computed only by the backend
    muted: bool
    drum_rack_visible: bool
    room_eq_enabled: bool


class SongStateManager:
    @classmethod
    def register(cls, song_state: SongState):
        song_state.title = song_state.title or get_window_title_from_filename(
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
        return next(filter(lambda s: s.title in title, cls.all()), None)  # type: ignore

    @classmethod
    def all(cls) -> List[SongState]:
        return list(_song_state_registry.values())


_song_state_registry: Dict[str, SongState] = {}


def get_focused_set() -> Optional[SongState]:
    if not is_ableton_focused():
        return None

    return SongStateManager.from_title(get_focused_window_title())
