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


def _overlapping_windows_to_audio_segment(windows: List[List[AudioSegment]]) -> AudioSegment:
    """ reduce overlapping AudioSegment windows to a single AudioSegment """
    audio_segment_array = list(map(lambda win: win[0], windows[:-1])) + windows[-1]
    return reduce(operator.add, audio_segment_array)


def _get_short_sounds_observable(source: AudioSourceInterface) -> Observable[AudioSegment]:
    """
        Make a ShortSound stream from an audio source
        A ShortSound is a chunk of signal that starts with high energy and ends with low energy

        This method windows source the stream in overlapping windows of List[AudioSegment]
        Then applies energy detection change to create List[List[AudioSegment]] chunks via an operator
        Which then maps the chunks to ShortSound
    """
    logger.info(f"making speech stream from source {source}")

    # windowing the audio source with overlapping windows
    return source.make_observable().pipe(
        op.buffer_with_count(RecordingConfig.WINDOW_SIZE, 1),
        ShortSoundDetection.short_sound_filter_map_operator
    )


def get_speech_recordings_observable(source: AudioSourceInterface) -> Observable[ShortSound]:
    return _get_short_sounds_observable(source=source).pipe(  # type: ignore
        op.filter(is_speech),
        op.map(SpeechSound),
        rx_debug("SpeechSound"),
        op.share()
    )
