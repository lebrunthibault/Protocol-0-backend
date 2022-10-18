import dataclasses
import json
from dataclasses import dataclass
from typing import List, Optional

import keyboard  # noqa
from dacite import from_dict
from loguru import logger

from api.midi_server.state import state_changed
from lib.ableton.ableton import is_ableton_focused
from lib.ableton.get_set import (
    get_launched_sets,
    get_recently_launched_set,
    get_window_title_from_filename,
)
from lib.redis import database
from lib.window.window import get_focused_window_title


@dataclass(frozen=True)
class AbletonSet:
    id: str
    set_title: str

    def __repr__(self):
        return f"AbletonSet('{self.set_title}')"

    @classmethod
    def register(cls, id):
        set_title = get_window_title_from_filename(get_recently_launched_set())

        if cls.from_title(set_title):
            logger.warning(f"Existing set {cls.from_title(set_title)}")
            return

        ableton_set = cls(id, set_title)
        _launched_sets.append(ableton_set)
        cls._persist()

    @classmethod
    def remove(cls, id):
        ableton_set = next(filter(lambda s: s.id == id, _launched_sets), None)
        if ableton_set is not None:
            _launched_sets.remove(ableton_set)
            cls._persist()

    @classmethod
    def from_title(cls, name: str) -> Optional["AbletonSet"]:
        return next(filter(lambda s: s.set_title in name, _launched_sets), None)  # type: ignore[arg-type]

    @classmethod
    def restore(cls):
        string_sets = database.get("ABLETON_SETS")
        logger.info(f"restoring ableton sets from database : {string_sets}")
        if string_sets is None:
            return []

        sets = [
            from_dict(data_class=AbletonSet, data=set_dict) for set_dict in json.loads(string_sets)
        ]

        _launched_sets[:] = list(filter(is_launched_set, sets))

    @classmethod
    def _persist(cls):
        database.set(
            "ABLETON_SETS", json.dumps([dataclasses.asdict(set) for set in _launched_sets])
        )
        state_changed.send()
        logger.info(f"persisted ableton sets: {cls.all()}")

    @classmethod
    def all(cls) -> List["AbletonSet"]:
        return _launched_sets


_launched_sets: List[AbletonSet] = []


def is_launched_set(set: AbletonSet) -> bool:
    for launched_set in get_launched_sets():
        if set.set_title in launched_set:
            return True

    return False


def get_focused_set() -> Optional[AbletonSet]:
    if not is_ableton_focused():
        return None

    return AbletonSet.from_title(get_focused_window_title())
