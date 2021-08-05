from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import scipy.fftpack as scp
from loguru import logger
from pydub import AudioSegment
from rx import operators as op
from rx.core.typing import Observable

from sr.audio.recording_config import RecordingConfig
from sr.audio.short_sound import ShortSound
from sr.audio.short_sound import get_short_sounds_observable
from sr.audio.sound_mixin import SoundMixin
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.rx.rx_utils import rx_debug

logger = logger.opt(colors=True)


@dataclass(frozen=True, repr=False)
class SpeechSound(SoundMixin):
    _short_sound: ShortSound

    @property
    def audio(self) -> AudioSegment:
        return self._short_sound.audio


def get_speech_sounds_observable(source: AudioSourceInterface) -> Observable[SpeechSound]:
    return get_short_sounds_observable(source=source).pipe(  # type: ignore
        op.filter(_is_speech),
        op.map(SpeechSound),
        rx_debug("SpeechSound"),
        op.share()
    )


@dataclass(frozen=True)
class FrequencyInfo():
    frequency: float
    energy: float


def _is_speech(sound: SoundMixin) -> bool:
    if not RecordingConfig.MINIMUM_SPEECH_DURATION < sound.duration_seconds < RecordingConfig.MAXIMUM_SPEECH_DURATION:
        logger.info(
            f"<yellow>Phrase duration not in the configured boundaries (lasted {sound.duration_seconds}s)</>"
        )
        return False

    strongest_frequency = _strongest_frequency(sound)
    if strongest_frequency.energy < RecordingConfig.MINIMUM_FREQUENCY_ENERGY:
        logger.info(
            f"<yellow>Didn't identify a voice, strongest frequency energy : {strongest_frequency.energy}</>"
        )
        return False

    return True


@lru_cache()
def _strongest_frequency(sound: SoundMixin) -> FrequencyInfo:
    # then normalize and convert to numpy array:
    x = np.double(list(sound.samples)) / (2 ** 15)
    X = np.abs(scp.fft(x))[0: int(len(x) / 2)]
    freq_window_start, freq_window_end = 50, 400
    frequency_energies = list(X[freq_window_start:freq_window_end])

    max_frequency_energy = max(frequency_energies)
    max_frequency = frequency_energies.index(max_frequency_energy) + RecordingConfig.SPEECH_FREQUENCY_WINDOW[0]

    return FrequencyInfo(frequency=max_frequency, energy=max_frequency_energy)
