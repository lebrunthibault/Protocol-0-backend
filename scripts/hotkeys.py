import logging
from typing import Callable

import keyboard

from scripts.commands.reload_ableton import reload_ableton


class HotKey():
    def __init__(self, hotkey: str, callback: Callable, suppress: bool = False):
        self._callback = callback
        self._hotkey = hotkey
        self._suppress = suppress
        keyboard.add_hotkey(self._hotkey, self._execute, suppress=self._suppress)
        logging.info(f"Registered {self}")

    def __repr__(self):
        return f"{self.__class__.__name__} {self._hotkey}: {self._callback.__name__}"

    @classmethod
    def add(cls, *a, **k):
        cls(*a, **k)

    def _execute(self):
        logging.info(f"{self} executing")
        self._callback()


class GlobalHotKey(HotKey):
    def __init__(self, *a, **k):
        super().__init__(suppress=True, *a, **k)


def setup_hotkeys():
    GlobalHotKey.add("ctrl+alt+shift+n", reload_ableton)
    keyboard.wait()


if __name__ == "__main__":
    setup_hotkeys()
