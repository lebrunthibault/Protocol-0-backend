import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.pyplot import figure

from sr.audio.recording import Recording

logger = logger.opt(colors=True)


class AudioPlot:
    Y_MAX = (2 ** 15) / 2

    @classmethod
    def plot_recording(cls, recording: Recording):
        figure(figsize=(10, 5))
        logger.disable(__name__)
        plt.plot(recording.samples, label="\n".join(recording.to_dict()))
        axes = plt.gca()
        axes.set_ylim([-cls.Y_MAX, cls.Y_MAX])
        plt.legend(loc="upper left")
        plt.show()
        logger.enable(__name__)
