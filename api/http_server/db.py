from typing import Optional, List

from pydantic import BaseModel


class SongState(BaseModel):
    drum_track_names: List[str]
    track_names: List[str]


class DB:
    SONG_STATE: Optional[SongState] = None
