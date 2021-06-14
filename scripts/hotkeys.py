import logging
from typing import Callable, Any

import keyboard

from scripts.commands.reload_ableton import reload_ableton


class HotKey():
    def __init__(self, hotkey: str, callback: Callable, suppress: bool = False) -> None:
        self._callback = callback
        self._hotkey = hotkey
        self._suppress = suppress
        keyboard.add_hotkey(self._hotkey, self._execute, suppress=self._suppress)
        logging.info(f"Registered {self}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self._hotkey}: {self._callback.__name__}"

    @classmethod
    def add(cls, *a: Any, **k: Any) -> None:
        cls(*a, **k)

    def _execute(self) -> None:
        logging.info(f"{self} executing")
        self._callback()


class GlobalHotKey(HotKey):
    def __init__(self, hotkey: str, callback: Callable):
        super().__init__(hotkey=hotkey, callback=callback, suppress=True)


def setup_hotkeys() -> None:
    GlobalHotKey.add("ctrl+alt+shift+n", reload_ableton)
    keyboard.wait()


if __name__ == "__main__":
    pass
    # setup_hotkeys()
