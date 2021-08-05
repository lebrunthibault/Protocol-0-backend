import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.pyplot import figure

from lib.utils import filename_datetime
from sr.audio.sound_mixin import SoundMixin
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def audio_export_sound(sound: SoundMixin) -> None:
    sound.export(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}\\raw\\{filename_datetime()}.wav")


def audio_plot_sound(sound: SoundMixin):
    Y_MAX = (2 ** 15) / 2

    figure(figsize=(10, 5))
    logger.disable(__name__)
    plt.plot(sound.samples, label="\n".join(sound.to_dict()))
    axes = plt.gca()
    axes.set_ylim([-Y_MAX, Y_MAX])
    plt.legend(loc="upper left")
    plt.show()
    logger.enable(__name__)
