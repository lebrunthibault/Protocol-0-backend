from typing import Optional, List

from pydantic import BaseModel


class SongState(BaseModel):
    drum_track_names: List[str]
    drum_categories: List[str]
    favorite_device_names: List[str]
    drum_rack_visible: bool


class DB:
    SONG_STATE: Optional[SongState] = None
