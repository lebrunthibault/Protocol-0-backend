import time
from typing import Optional, List

from api.p0_script_api_client import protocol0
from lib.ableton import reload_ableton
from loguru import logger

from lib.utils import copy_to_clipboard


class AbletonSetProfilingSession():
    """ we skip the first test as it is not in the average """
    def __init__(self, number_of_tests):
        self.number_of_tests = number_of_tests
        self.last_set_reloaded_at: Optional[float] = None
        self.measurements = []  # type: List[float]

    def __repr__(self):
        return self.to_csv

    @property
    def to_csv(self):
        return ",".join(["%.2f" % m for m in self.measurements[1:]])

    @property
    def to_google_sheet_formula(self):
        return f'=SPLIT("{self.to_csv}", ",")'

    @property
    def finished(self) -> bool:
        if self.number_of_tests == 1:
            return True
        return len(self.measurements) >= self.number_of_tests + 1

    def start_measurement(self):
        self.last_set_reloaded_at = time.time()
        reload_ableton()

    def end_measurement(self):
        reload_duration = time.time() - self.last_set_reloaded_at
        self.measurements.append(reload_duration)

        if self.finished:
            logger.info(self.to_csv)
            copy_to_clipboard(self.to_google_sheet_formula)
            logger.info(f"{self.to_google_sheet_formula} copied to clipboard")
            protocol0.show_message(f"reload session over : {self.to_csv}")
        else:
            logger.info(f"Measurement {len(self.measurements) + 1}/{self.number_of_tests} finished, got %.2f s" % reload_duration)
            protocol0.show_message("set reloaded in %.2f s" % reload_duration)
            self.start_measurement()
