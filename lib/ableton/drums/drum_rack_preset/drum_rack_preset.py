from os.path import dirname
from typing import List

from jinja2 import Template

from lib.ableton.drums.drum_rack_preset.drum_branch.drum_branch_preset import DrumBranchPreset


class DrumRackPreset():
    def __init__(self, drum_category: str, drum_names: List[str]):
        self._drum_category = drum_category
        self._drum_names = drum_names

    def to_xml(self) -> str:
        drum_branch_presets = []
        for i, drum_name in enumerate(self._drum_names):
            drum_branch_presets.append(DrumBranchPreset(self._drum_category, drum_name, i).to_xml())

        with open(f"{dirname(__file__)}/drum_rack_preset.xml", "r") as f:
            t = Template(f.read())
            return t.render({"drum_branch_presets": drum_branch_presets})
