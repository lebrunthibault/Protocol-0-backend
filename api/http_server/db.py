from typing import Optional

from api.http_server.model.song_state import SongState


class DB:
    song_state: Optional[SongState] = None
