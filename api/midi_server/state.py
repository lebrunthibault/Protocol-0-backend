import requests
from blinker import signal

from config import Config

state_changed = signal("state-changed")


def _on_state_changed(_):
    requests.get(f"{Config.HTTP_API_URL}/sync")


state_changed.connect(_on_state_changed)
