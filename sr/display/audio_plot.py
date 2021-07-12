import matplotlib.pyplot as plt
from lib.observable import Event
from loguru import logger
from matplotlib.pyplot import figure

from speech_recognition.audio_data.Recording import Recording


class AudioPlot:
    Y_MAX = 16384

    @classmethod
    def receive_recorder_event(cls, event: Event):
        if not isinstance(event.data, Recording):
            return
        recording = event.data
        legend = [
            f"duration: {recording.duration:.3f}",
            f"minimum_duration: {recording.config.minimum_duration:.1f}",
            f"dBFS: {recording.pydub_sound.dBFS:.1f}",
            f"start dbFS: {recording.start_window_dbfs:.1f}",
            f"end dbFS: {recording.end_window_dbfs:.1f}",
            f"freq maximum: {recording.maximum_voice_frequency:.1f}",
            f"freq maximum energy: {recording.maximum_voice_frequency_energy:.1f}",
        ]

        figure(figsize=(10, 5))
        logger.disable(__name__)
        plt.plot(recording.array_data, label="\n".join(legend))
        axes = plt.gca()
        axes.set_ylim([-cls.Y_MAX, cls.Y_MAX])
        plt.legend(loc="upper left")
        # plt.text(x=0, y=cls.Y_MAX / 2, s=legend, fontsize=20)
        plt.show()
        logger.enable(__name__)
