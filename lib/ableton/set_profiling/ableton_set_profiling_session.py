import time
from typing import Optional, List

from loguru import logger
from protocol0.application.command.ShowMessageCommand import ShowMessageCommand

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.ableton import reload_ableton
from lib.utils import copy_to_clipboard


class AbletonSetProfilingSession:
    """we skip the first test as it is not in the average"""

    def __init__(self, number_of_tests):
        self.number_of_tests = number_of_tests
        self.last_set_reloaded_at: Optional[float] = None
        self.measurements = []  # type: List[float]

    def __repr__(self):
        return self._to_csv

    def show_message(self, message: str):
        p0_script_client().dispatch(ShowMessageCommand(message))

    @property
    def _single_test(self):
        return self.number_of_tests == 1

    @property
    def _to_csv(self):
        return ",".join(["%.2f" % m for m in self.measurements[1:]])

    @property
    def _to_google_sheet_formula(self):
        return f'=SPLIT("{self._to_csv}", ",")'

    @property
    def _is_finished(self) -> bool:
        return len(self.measurements) >= self.number_of_tests + 1

    def start_measurement(self):
        self.last_set_reloaded_at = time.time()
        reload_ableton()

    def end_measurement(self):
        reload_duration = time.time() - self.last_set_reloaded_at
        self.show_message("set reloaded in %.2f s" % reload_duration)

        if self._single_test:
            return

        self.measurements.append(reload_duration)

        if self._is_finished:
            copy_to_clipboard(self._to_google_sheet_formula)
            logger.info(f"{self._to_google_sheet_formula} copied to clipboard")
            self.show_message(f"set profiling over : {self._to_csv}")
        else:
            logger.info(
                f"Measurement {len(self.measurements) + 1}/{self.number_of_tests} finished, got %.2f s"
                % reload_duration
            )
            self.show_message("set reloaded in %.2f s" % reload_duration)
            self.start_measurement()
