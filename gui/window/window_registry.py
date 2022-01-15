from typing import Optional

from gui.window.window import Window


class WindowRegistry:
    _CURRENT_INSTANCE: Optional[Window] = None

    @classmethod
    def close_current_window(cls):
        print(f"in close_current_window: {cls._CURRENT_INSTANCE}")
        if cls._CURRENT_INSTANCE:
            cls._CURRENT_INSTANCE.sg_window.close()
            cls._CURRENT_INSTANCE = None
