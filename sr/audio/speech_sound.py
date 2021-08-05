from dataclasses import dataclass

from loguru import logger
from pydub import AudioSegment

from sr.audio.short_sound import ShortSound
from sr.audio.sound_mixin import SoundMixin

logger = logger.opt(colors=True)


@dataclass(frozen=True, repr=False)
class SpeechSound(SoundMixin):
    _short_sound: ShortSound

    @property
    def audio(self) -> AudioSegment:
        return self._short_sound.audio
