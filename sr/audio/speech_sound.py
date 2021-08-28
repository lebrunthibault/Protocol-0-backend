from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import scipy.fftpack as scp
from loguru import logger
from pydub import AudioSegment
from pysndfx import AudioEffectsChain
from rx import operators as op
from rx.core.typing import Observable

from sr.audio.recording_config import RecordingConfig
from sr.audio.short_sound import get_short_sounds_observable
from sr.audio.sound_mixin import SoundMixin
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.rx.rx_utils import rx_debug

logger = logger.opt(colors=True)


@dataclass(frozen=True, repr=False)
class SpeechSound(SoundMixin):
    audio: AudioSegment


def _maximize_audio(audio: AudioSegment) -> AudioSegment:
    """ See http://sox.sourceforge.net/sox.html """
    fx = AudioEffectsChain()

    # noise gate
    fx.command.append('compand')
    attack, decay = 0.1, 0.2
    fx.command.append(f"{attack},{decay}")
    fx.command.append("-inf,-50.1,-inf,-50,-50")

    fx.normalize()
    # fx.limiter(gain=3)
    buffer = fx(np.array(audio.get_array_of_samples()))
    return AudioSegment(data=buffer.tobytes(), sample_width=audio.sample_width,
                        frame_rate=audio.frame_rate, channels=1)


def get_speech_sounds_observable(source: AudioSourceInterface) -> Observable[SpeechSound]:
    return get_short_sounds_observable(source=source).pipe(  # type: ignore
        op.filter(_is_speech),
        op.map(lambda short_sound: SpeechSound(_maximize_audio(short_sound.audio))),
        rx_debug("SpeechSound"),
        op.share()
    )


@dataclass(frozen=True)
class FrequencyInfo:
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
    samples = np.double(list(sound.samples)) / (2 ** 15)
    fft_samples = np.abs(scp.fft(samples))[0: int(len(samples) / 2)]
    freq_window_start, freq_window_end = 50, 400
    frequency_energies = list(fft_samples[freq_window_start:freq_window_end])

    max_frequency_energy = max(frequency_energies)
    max_frequency = frequency_energies.index(max_frequency_energy) + RecordingConfig.SPEECH_FREQUENCY_WINDOW[0]

    return FrequencyInfo(frequency=max_frequency, energy=max_frequency_energy)
