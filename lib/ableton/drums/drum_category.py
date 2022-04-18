import json
import os
from typing import List

from loguru import logger
from pydub import AudioSegment

from config import Config


class DrumCategory():
    def __init__(self, directory: str, sample_names: List[str]):
        self._directory = directory
        self._sample_names = sample_names

    def __repr__(self) -> str:
        return self.name

    @classmethod
    def create_all(cls) -> List["DrumCategory"]:
        categories = []
        for root, _, files in os.walk(Config.SAMPLE_DIRECTORY):
            if root == Config.SAMPLE_DIRECTORY or os.path.basename(root).startswith("_"):
                continue

            samples = [s for s in files if s.endswith(".wav") and not s.startswith("_")]
            categories.append(DrumCategory(root, samples))

        return categories

    @property
    def name(self) -> str:
        return os.path.basename(self._directory).lower()

    @property
    def samples_info(self) -> List[str]:
        if not os.path.exists(self.samples_info_path):
            return []

        with open(self.samples_info_path, "r") as f:
            return json.loads(f.read())

    @property
    def full_sample_path(self) -> str:
        return f"{self._directory}\\_{self.name}_full.wav"

    @property
    def samples_info_path(self) -> str:
        return f"{self._directory}\\_{self.name}_info.json"

    @property
    def is_synced(self) -> bool:
        """Returns True if samples in the directory are the same as in the sample info file"""
        return self._sample_names == self.samples_info

    def sync_drum_rack_full_sample(self):
        full_sample = AudioSegment.empty()

        for sample in self._sample_names:
            full_sample += AudioSegment.from_wav(f"{self._directory}\\{sample}")
            full_sample += AudioSegment.silent(duration=2000)

        full_sample = full_sample.set_sample_width(2)

        # cache the sample names
        with open(self.samples_info_path, "w") as f:
            f.write(json.dumps(self._sample_names))

        full_sample.export(self.full_sample_path, format="wav")
        logger.info(f"{self} synced")
