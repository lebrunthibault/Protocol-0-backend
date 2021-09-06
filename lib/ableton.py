from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AbletonInfos():
    ableton_version: str

    @property
    def ableton_major_version(self) -> str:
        return self.ableton_version.split('.')[0]

    @property
    def program_name(self) -> str:
        return f"Ableton Live {self.ableton_major_version} Suite"

    @property
    def log_file_location(self) -> Path:
        return Path("")

    @property
    def preferences_location(self) -> Path:
        return Path(f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {self.ableton_version}\Preferences")

    @property
    def exe_location(self) -> Path:
        return Path(f"C:\\ProgramData\\Ableton\\Live {self.ableton_major_version}\\Program\\Ableton Live {self.ableton_major_version} Suite.exe")
