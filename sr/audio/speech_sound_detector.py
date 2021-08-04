from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import scipy.fftpack as scp
from loguru import logger
from sr.audio.recording_config import RecordingConfig
from sr.audio.short_sound import ShortSound

logger = logger.opt(colors=True)


@dataclass(frozen=True)
class FrequencyInfo():
    frequency: float
    energy: float


def is_speech(short_sound: ShortSound) -> bool:
    if not RecordingConfig.MINIMUM_SPEECH_DURATION < short_sound.duration_seconds < RecordingConfig.MAXIMUM_SPEECH_DURATION:
        logger.info(
            f"<yellow>Phrase duration not in the configured boundaries (lasted {short_sound.duration_seconds}s)</>"
        )
        return False

    strongest_frequency = _strongest_frequency(short_sound)
    if strongest_frequency.energy < RecordingConfig.MINIMUM_FREQUENCY_ENERGY:
        logger.info(
            f"<yellow>Didn't identify a voice, strongest frequency energy : {strongest_frequency.energy}</>"
        )
        return False

    return True


@lru_cache()
def _strongest_frequency(short_sound: ShortSound) -> FrequencyInfo:
    # then normalize and convert to numpy array:
    x = np.double(list(short_sound.samples)) / (2 ** 15)
    X = np.abs(scp.fft(x))[0: int(len(x) / 2)]
    freq_window_start, freq_window_end = 50, 400
    frequency_energies = list(X[freq_window_start:freq_window_end])

    max_frequency_energy = max(frequency_energies)
    max_frequency = frequency_energies.index(max_frequency_energy) + RecordingConfig.SPEECH_FREQUENCY_WINDOW[0]

    return FrequencyInfo(frequency=max_frequency, energy=max_frequency_energy)
