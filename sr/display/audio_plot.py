import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.pyplot import figure

from sr.audio.recording import Recording

logger = logger.opt(colors=True)


class AudioPlot:
    Y_MAX = (2 ** 15) / 2

    @classmethod
    def plot_recording(cls, recording: Recording):
        legend = [
            f"duration: {recording.audio.duration_seconds:.3f}",
            f"minimum_duration: {recording.config.minimum_duration:.1f}",
            f"dBFS: {recording.audio.dBFS:.1f}",
            f"start dbFS: {recording.start_window.dBFS:.1f}",
            f"end dbFS: {recording.end_window.dBFS:.1f}",
            f"freq maximum: {recording.maximum_voice_frequency:.1f}",
            f"freq maximum energy: {recording.maximum_voice_frequency_energy:.1f}",
        ]

        figure(figsize=(10, 5))
        logger.disable(__name__)
        plt.plot(recording.audio.get_array_of_samples(), label="\n".join(legend))
        axes = plt.gca()
        axes.set_ylim([-cls.Y_MAX, cls.Y_MAX])
        plt.legend(loc="upper left")
        # plt.text(x=0, y=cls.Y_MAX / 2, s=legend, fontsize=20)
        plt.show()
        logger.enable(__name__)
