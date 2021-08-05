from dataclasses import dataclass

from loguru import logger
from pydub import AudioSegment

from sr.audio.sound_mixin import SoundMixin

logger = logger.opt(colors=True)


@dataclass(frozen=True, repr=False)
class ShortSound(SoundMixin):
    _audio_segment: AudioSegment

    # def to_dict(self):
    #     return {**super().to_dict(),
    #             f"strongest frequency: {self._strongest_frequency}",
    #             }

    @property
    def audio(self) -> AudioSegment:
        return self._audio_segment
