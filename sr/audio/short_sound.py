import operator
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import List, Any

from loguru import logger
from pydub import AudioSegment
from rx import operators as op, create
from rx.core.typing import Observable

from sr.audio.recording_config import RecordingConfig
from sr.audio.sound_mixin import SoundMixin
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.rx.rx_utils import rx_debug

logger = logger.opt(colors=True)


@dataclass(frozen=True, repr=False)
class ShortSound(SoundMixin):
    audio: AudioSegment


def get_short_sounds_observable(source: AudioSourceInterface) -> Observable[ShortSound]:
    """
        Make a ShortSound stream from an audio source
        A ShortSound is a chunk of signal that starts with high energy and ends with low energy

        This method windows source the stream in overlapping windows of List[AudioSegment]
        Then applies energy detection change to create List[List[AudioSegment]] chunks via an operator
        Which then maps the chunks to ShortSound
    """
    logger.info(f"making speech stream from source {source}")

    # windowing the audio source with overlapping windows
    windows = source.make_observable().pipe(
        op.buffer_with_count(RecordingConfig.WINDOW_SIZE, 1),
        op.share()
    )

    # detecting energy changes in the signal
    energy_change_obs = windows.pipe(AudioEnergyChangeDetection.energy_change_operator, op.share())
    recording_window_openings = energy_change_obs.pipe(op.filter(lambda energy: energy == AudioEnergyEnum.HIGH))
    recording_window_closings = energy_change_obs.pipe(op.filter(lambda energy: energy == AudioEnergyEnum.LOW))

    # creating short sound chunks
    return windows.pipe(
        op.buffer_toggle(recording_window_openings, lambda _: recording_window_closings),
        op.map(_overlapping_windows_to_audio_segment),
        op.map(ShortSound),
        rx_debug("ShortSound"),
    )


class AudioEnergyEnum(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AudioEnergyChangeDetection():
    CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW
    DEBUG = False

    @classmethod
    def energy_change_operator(cls, source: Observable) -> Observable:
        def high_energy_change_observable(observer, _) -> Any:
            def analyze(window: List[AudioSegment]):
                previous_buffer_energy = cls.CURRENT_BUFFER_ENERGY
                audio_segment = sum(window)

                if audio_segment.dBFS >= RecordingConfig.HIGH_ENERGY_THRESHOLD_DBFS:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.HIGH
                elif audio_segment.dBFS < RecordingConfig.LOW_ENERGY_THRESHOLD_DBFS:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW

                if cls.DEBUG:
                    logger.info(f"current buf energy: {audio_segment.dBFS} {cls.CURRENT_BUFFER_ENERGY}")

                if previous_buffer_energy != cls.CURRENT_BUFFER_ENERGY:
                    observer.on_next(cls.CURRENT_BUFFER_ENERGY)

            return source.subscribe(analyze, observer.on_error, observer.on_completed)

        return create(high_energy_change_observable)


def _overlapping_windows_to_audio_segment(windows: List[List[AudioSegment]]) -> AudioSegment:
    """ reduce overlapping AudioSegment windows to a single AudioSegment """
    audio_segment_array = list(map(lambda win: win[0], windows[:-1])) + windows[-1]
    return reduce(operator.add, audio_segment_array)
