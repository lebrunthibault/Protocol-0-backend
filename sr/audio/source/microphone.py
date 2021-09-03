import asyncio
from typing import Optional

import pyaudio
from loguru import logger
# from loguru import logger
from pyaudio import Stream
from pydub import AudioSegment
from rx import Observable

from sr.audio.recording_config import RecordingConfig
from sr.audio.source.audio_source_interface import AudioSourceInterface
# noinspection PyBroadException
from lib.rx import rx_obs_from_async_iterable


class Microphone(AudioSourceInterface):
    """
    If ``device_index`` is unspecified or ``None``, the default microphone is used as the audio source. Otherwise, ``device_index`` should be the index of the device to use for audio input.
    See the `PyAudio documentation <https://people.csail.mit.edu/hubert/pyaudio/docs/>`__ for more details.
    The microphone audio is recorded in chunks of ``chunk_size`` samples, at a rate of ``sample_rate`` samples per second (Hertz).
    If not specified, the value of ``sample_rate`` is determined automatically from the system's microphone settings.
    Higher ``chunk_size`` values help avoid triggering on rapidly changing ambient noise, but also makes detection less sensitive.
    This value, generally, should be left at its default.
    """

    def __init__(self, device_index=None, sample_rate=None, chunk_size=1024):
        assert device_index is None or isinstance(device_index, int), "Device index must be None or an integer"
        assert sample_rate is None or (
            isinstance(sample_rate, int) and sample_rate > 0
        ), "Sample rate must be None or a positive integer"
        assert isinstance(chunk_size, int) and chunk_size > 0, "Chunk size must be a positive integer"

        # set up PyAudio
        self.pyaudio_module = self.get_pyaudio()
        audio = self.pyaudio_module.PyAudio()
        logger.info("pyaudio loaded")
        try:
            count = audio.get_device_count()  # obtain device count
            if device_index is not None:  # ensure device index is in range
                assert (
                    0 <= device_index < count
                ), "Device index out of range ({} devices available; device index should be between 0 and {} inclusive)".format(
                    count, count - 1
                )
            if (
                sample_rate is None
            ):  # automatically set the sample rate to the hardware's default sample rate if not specified
                device_info = (
                    audio.get_device_info_by_index(device_index)
                    if device_index is not None
                    else audio.get_default_input_device_info()
                )
                assert (
                    isinstance(device_info.get("defaultSampleRate"), (float, int))
                    and device_info["defaultSampleRate"] > 0
                ), "Invalid device info returned from PyAudio: {}".format(device_info)
                sample_rate = int(device_info["defaultSampleRate"])
        finally:
            audio.terminate()

        self.device_index = device_index
        self.device_info = device_info
        self.name = device_info["name"]
        self.format = self.pyaudio_module.paInt16  # 16-bit int sampling
        self.sample_width = self.pyaudio_module.get_sample_size(self.format)  # size of each sample
        self.sample_rate = sample_rate  # sampling rate in Hertz
        self.chunk_size = chunk_size  # number of frames stored in each buffer

        self.audio = None
        self.stream: Optional[MicrophoneStream] = None
        self._open_stream()

    @staticmethod
    def get_pyaudio():
        """
        Imports the pyaudio module and checks its version. Throws exceptions if pyaudio can't be found or a wrong version is installed
        """
        try:
            import pyaudio
        except ImportError:
            raise AttributeError("Could not find PyAudio; check installation")
        from distutils.version import LooseVersion

        if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.11"):
            raise AttributeError("PyAudio 0.2.11 or later is required (found version {})".format(pyaudio.__version__))
        return pyaudio

    def _open_stream(self):
        assert self.stream is None, "This audio source stream was already opened"
        self.audio = self.pyaudio_module.PyAudio()
        try:
            pyaudio_stream = self.audio.open(
                input_device_index=self.device_index,
                channels=1,
                format=self.format,
                rate=self.sample_rate,
                frames_per_buffer=self.chunk_size,
                input=True,
            )
        except Exception as e:
            logger.error(f"Exception while opening Microphone pyaudio stream : {e}")
            logger.error(pyaudio.get_sample_size())
            self.audio.terminate()
            raise e

        self.stream = MicrophoneStream(pyaudio_stream=pyaudio_stream)

    def close(self):
        try:
            self.stream.close()
        finally:
            self.stream = None
            self.audio.terminate()

    def make_observable(self) -> Observable:
        logger.info("creating microphone observable")
        return rx_obs_from_async_iterable(self.read())

    async def read(self):
        while True:
            window_size = int((self.sample_rate / 1000) * RecordingConfig.BUFFER_MS)
            try:
                buffer = self.stream.read(window_size)
            except OSError as e:
                # happens when windows goes to sleep
                logger.error(e)
                await asyncio.sleep(1)
                continue
            yield AudioSegment(data=buffer, sample_width=self.sample_width,
                               frame_rate=self.sample_rate, channels=1)


class MicrophoneStream(object):
    def __init__(self, pyaudio_stream: Stream):
        self.pyaudio_stream = pyaudio_stream

    def read(self, size):
        return self.pyaudio_stream.read(size, exception_on_overflow=False)

    def close(self):
        try:
            # sometimes, if the stream isn't stopped, closing the stream throws an exception
            if not self.pyaudio_stream.is_stopped():
                self.pyaudio_stream.stop_stream()
        finally:
            self.pyaudio_stream.close()
