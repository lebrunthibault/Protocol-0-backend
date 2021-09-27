class RecordingConfig:
    BUFFER_MS = 20
    # buffer window to consider for identifying phrase start and end
    WINDOW_MS = 300  # ms
    WINDOW_SIZE = WINDOW_MS / BUFFER_MS
    HIGH_ENERGY_THRESHOLD_DBFS = -40  # minimum dbfs volume to consider high energy
    LOW_ENERGY_THRESHOLD_DBFS = -50  # maximum dbfs volume to consider low energy
    MINIMUM_FREQUENCY_ENERGY = 20  # identify speech vs noise
    # pause_threshold = 0.1  # seconds of non-speaking audio before a phrase is considered complete
    # # minimum seconds of speaking audio before we consider the speaking audio a phrase
    # # - values below this are ignored (for filtering out clicks and pops)
    MINIMUM_SPEECH_DURATION = 0.2  # seconds
    MAXIMUM_SPEECH_DURATION = 2  # seconds

    SPEECH_FREQUENCY_WINDOW = (50, 400)
