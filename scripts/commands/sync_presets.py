import logging
import os
from typing import Generator, Any


class SerumPresetSynchronizer:
    PRESET_DIRECTORY = "C:\\Users\\thiba\\OneDrive\\Documents\\Xfer\\Serum Presets\\Presets\\"
    PROGRAM_CHANGE_FILENAME = "C:\\Users\\thiba\\OneDrive\\Documents\\Xfer\\Serum Presets\\System\\ProgramChanges.txt"

    @classmethod
    def get_preset_names(cls):
        # type: () -> Generator[str, Any, Any]
        for path, _, files in os.walk(cls.PRESET_DIRECTORY):
            relative_path = path.replace(cls.PRESET_DIRECTORY, "")
            if not relative_path or relative_path.startswith("_"):
                continue

            for name in files:
                if not name.endswith(".fxp"):
                    continue
                yield os.path.join(relative_path, name)

    @classmethod
    def synchronize(cls):
        # type: () -> str
        presets = list(cls.get_preset_names())
        with open(cls.PROGRAM_CHANGE_FILENAME, "w") as f:
            for preset in presets:
                f.write("%s\n" % preset)

        res = "%d serum presets wrote to %s" % (len(presets), cls.PROGRAM_CHANGE_FILENAME)
        logging.info(res)
        return res


def sync_presets() -> str:
    return SerumPresetSynchronizer.synchronize()
