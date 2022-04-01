import json
from typing import Dict

import requests
from loguru import logger

from config import Config


class SongState():
    """Song state as seen from the midi server"""

    def __init__(self):
        self._state: Dict = {}

    def to_json(self):
        return json.dumps(self._state)

    def update(self, state: Dict):
        self._state = state
        self._notify_http()

    def _notify_http(self):
        logger.info(f"notifying {self.to_json()}")
        requests.post(f"{Config.HTTP_API_URL}/song_state", data=self.to_json())
