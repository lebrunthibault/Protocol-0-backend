from typing import List, Dict

from pydantic import BaseModel


class SongState(BaseModel):
    drum_track_names: List[str]
    sample_categories: Dict[str, List[str]]
    favorite_device_names: List[List[str]]
    insert_favorite_device_names: List[str]
    drum_rack_visible: bool
    room_eq_enabled: bool
