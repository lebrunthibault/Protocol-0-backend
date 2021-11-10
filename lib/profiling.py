import time
from typing import Optional

from api.p0_script_api_client import p0_script_api_client


class AbletonSetProfiler():
    last_set_reloaded_at: Optional[float] = None

    @classmethod
    def store_set_reloaded_at(cls):
        cls.last_set_reloaded_at = time.time()
        print(cls.last_set_reloaded_at)

    @classmethod
    def display_last_ableton_set_duration(cls):
        if not AbletonSetProfiler.last_set_reloaded_at:
            p0_script_api_client.show_message("No reload time set")
            return

        reload_duration = time.time() - AbletonSetProfiler.last_set_reloaded_at
        p0_script_api_client.show_message("set reloaded in %.2f s" % reload_duration)
