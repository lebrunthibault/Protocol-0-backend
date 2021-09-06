import shutil
import subprocess

from config import SystemConfig
from lib.ableton import AbletonInfos
from lib.process import kill_window_by_criteria
from lib.window.find_window import SearchTypeEnum
ableton_locations = AbletonInfos(ableton_version=SystemConfig.ABLETON_VERSION)


def restart_ableton():
    # kill ableton
    kill_window_by_criteria(name=ableton_locations.program_name, search_type=SearchTypeEnum.WINDOW_TITLE)

    # remove crash files
    shutil.rmtree(ableton_locations.preferences_location / "Crash")
    (ableton_locations.preferences_location / "CrashDetection.cfg").unlink()
    (ableton_locations.preferences_location / "CrashRecoveryInfo.cfg").unlink()
    (ableton_locations.preferences_location / "Log.txt").unlink()

    # restart
    subprocess.run([ableton_locations.exe_location])
