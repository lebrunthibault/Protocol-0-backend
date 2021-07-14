from speech_recognition.audio_source.AbstractAudioSource import AbstractAudioSource


class RecordingConfig():
    def __init__(self, source: AbstractAudioSource):
        # buffer window to consider for identifying phrase start and end
        self.start_window_duration = 0.1  # seconds
        self.start_window_count = self.start_window_duration * source.SAMPLE_RATE
        self.minimum_dbfs = -35  # minimum dbfs volume to consider speak
        self.minimum_frequency_energy = 80  # identify voice vs noise
        # self.pause_threshold = 0.1  # seconds of non-speaking audio before a phrase is considered complete
        # # minimum seconds of speaking audio before we consider the speaking audio a phrase
        # # - values below this are ignored (for filtering out clicks and pops)
        self.minimum_duration = 0.2  # seconds
        self.maximum_duration = 600  # seconds
        self.seconds_per_buffer = float(source.CHUNK_SIZE) / source.SAMPLE_RATE
