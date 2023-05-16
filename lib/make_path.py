import sys
import os

from api.settings import Settings

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(
    0,
    f"C:\ProgramData\Ableton\Live {Settings().ableton_major_version} Suite\Resources\MIDI Remote Scripts",
)
sys.path.insert(0, "C:\\Users\\thiba\\dev\\protocol0_stream_deck")
