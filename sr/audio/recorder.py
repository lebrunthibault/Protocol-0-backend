import operator
from enum import Enum
from functools import reduce
from typing import List, Any

from loguru import logger
from pydub import AudioSegment
from rx import operators as op, create
from rx.core.typing import Observable

from sr.audio.recording_config import RecordingConfig
from sr.audio.short_sound import ShortSound
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.audio.speech_sound import SpeechSound
from sr.audio.speech_sound_detector import is_speech
from sr.rx.rx_utils import rx_debug

logger = logger.opt(colors=True)


class AudioEnergyEnum(Enum):
    LOW = "LOW"
    HIGH = "HIGH"


class ShortSoundDetection():
    CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW
    CURRENT_CHUNK = []
    DEBUG = False

    @classmethod
    def short_sound_filter_map_operator(cls, source: Observable) -> Observable:
        def short_sound_observable(observer, _) -> Any:
            def analyze(window: List[AudioSegment]):
                previous_buffer_energy = cls.CURRENT_BUFFER_ENERGY
                # print(audio_segment, audio_segment.duration_seconds)

                if sum(window).dBFS >= RecordingConfig.MINIMUM_DBFS:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.HIGH
                    cls.CURRENT_CHUNK.append(window)
                else:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW

                if cls.DEBUG:
                    logger.info(f"current buf energy: {cls.CURRENT_BUFFER_ENERGY}")

                if previous_buffer_energy == AudioEnergyEnum.HIGH and cls.CURRENT_BUFFER_ENERGY == AudioEnergyEnum.LOW:
                    audio_segment = _overlapping_windows_to_audio_segment(cls.CURRENT_CHUNK)
                    recording = ShortSound(audio_segment)
                    observer.on_next(recording)
                    cls.CURRENT_CHUNK = []

            return source.subscribe(analyze, observer.on_error, observer.on_completed)

        return create(short_sound_observable)


class AudioEnergyChangeDetection():
    CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW
    DEBUG = False

    @classmethod
    def energy_change_operator(cls, source: Observable) -> Observable:
        def high_energy_change_observable(observer, _) -> Any:
            def analyze(window: List[AudioSegment]):
                previous_buffer_energy = cls.CURRENT_BUFFER_ENERGY
                audio_segment = sum(window)

                if audio_segment.dBFS >= RecordingConfig.MINIMUM_DBFS:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.HIGH
                else:
                    cls.CURRENT_BUFFER_ENERGY = AudioEnergyEnum.LOW

                if cls.DEBUG:
                    logger.info(f"current buf energy: {audio_segment.dBFS} {cls.CURRENT_BUFFER_ENERGY}")

                if previous_buffer_energy != cls.CURRENT_BUFFER_ENERGY:
                    observer.on_next(cls.CURRENT_BUFFER_ENERGY)

            return source.subscribe(analyze, observer.on_error, observer.on_completed)

        return create(high_energy_change_observable).pipe(rx_debug("energy_change"))


def _overlapping_windows_to_audio_segment(windows: List[List[AudioSegment]]) -> AudioSegment:
    """ reduce overlapping AudioSegment windows to a single AudioSegment """
    audio_segment_array = list(map(lambda win: win[0], windows[:-1])) + windows[-1]
    return reduce(operator.add, audio_segment_array)


def get_short_sounds_observable(source: AudioSourceInterface) -> Observable[AudioSegment]:
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
        op.map(ShortSound)
    )

    # # windowing the audio source with overlapping windows
    # return source.make_observable().pipe(
    #     op.buffer_with_count(RecordingConfig.WINDOW_SIZE, 1),
    #     ShortSoundDetection.short_sound_filter_map_operator,
    #     rx_debug("ShortSound")
    # )


def get_speech_sounds_observable(source: AudioSourceInterface) -> Observable[ShortSound]:
    return get_short_sounds_observable(source=source).pipe(  # type: ignore
        op.filter(is_speech),
        op.map(SpeechSound),
        rx_debug("SpeechSound"),
        op.share()
    )
