from typing import Optional

from loguru import logger

from api.p0_script_api_client import protocol0, APIMessageSender
from config import SystemConfig
from lib.ableton_set_profiling.ableton_set_profiling_session import AbletonSetProfilingSession
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


class AbletonSetProfiler():
    NUMBER_OF_TESTS = 5
    last_set_reloaded_at: Optional[float] = None
    current_profiling_session: Optional[AbletonSetProfilingSession] = None

    @classmethod
    def handle_profiling_error(cls, message: str):
        logger.error(message)
        protocol0.show_message(message)

    @classmethod
    def check_profiling_conditions(cls):
        if find_window_handle_by_enum(SystemConfig.LOG_WINDOW_TITLE, SearchTypeEnum.WINDOW_TITLE) != 0:
            cls.handle_profiling_error("Close the log window to start profiling")
            return False
        return True

    @classmethod
    def start_set_profiling(cls, number_of_tests=None, check_profiling_conditions=True):
        if check_profiling_conditions and not cls.check_profiling_conditions():
            return
        cls.current_profiling_session = AbletonSetProfilingSession(
            number_of_tests=number_of_tests or cls.NUMBER_OF_TESTS)
        cls.current_profiling_session.start_measurement()

    @classmethod
    def start_profiling_single_measurement(cls):
        cls.start_set_profiling(number_of_tests=1, check_profiling_conditions=False)

    @classmethod
    def end_measurement(cls):
        if not cls.current_profiling_session:
            protocol0.show_message("No active profiling session")
            return
        cls.current_profiling_session.end_measurement()
        if cls.current_profiling_session._is_finished:
            cls.current_profiling_session = None
