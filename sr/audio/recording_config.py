from sr.audio.source.audio_source_interface import AudioSourceInterface


class RecordingConfig:
    def __init__(self, source: AudioSourceInterface):
        # buffer window to consider for identifying phrase start and end
        self.start_window_duration = 100  # ms
        self.minimum_dbfs = -35  # minimum dbfs volume to consider speak
        self.minimum_frequency_energy = 80  # identify speech vs noise
        # self.pause_threshold = 0.1  # seconds of non-speaking audio before a phrase is considered complete
        # # minimum seconds of speaking audio before we consider the speaking audio a phrase
        # # - values below this are ignored (for filtering out clicks and pops)
        self.minimum_duration = 0.2  # seconds
        self.maximum_duration = 2  # seconds
