from os.path import dirname

from lib.observable import Event
from lib.utils import filename_datetime

from speech_recognition.audio_data.Recording import Recording


class AudioExport():
    EXPORT_DIRECTORY = f"{dirname(__file__)}/audio"

    @classmethod
    def receive_recorder_event(cls, event: Event) -> None:
        if not isinstance(event.data, Recording):
            return
        recording = event.data
        filename = f"{cls.EXPORT_DIRECTORY}/{filename_datetime()}.wav"
        return recording.pydub_sound.export(filename,
                                            format="wav"
                                            )
