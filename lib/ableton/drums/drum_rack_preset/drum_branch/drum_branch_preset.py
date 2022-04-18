from os.path import dirname

from jinja2 import Template


class DrumBranchPreset():
    def __init__(self, drum_category: str, drum_name: str, index: int):
        self._drum_category = drum_category
        self._drum_name = drum_name
        self._index = index

    def to_xml(self) -> str:
        with open(f"{dirname(__file__)}/drum_branch_preset.xml", "r") as f:
            t = Template(f.read())
            return t.render({"drum_category": self._drum_category, "drum_name": self._drum_name, "index": self._index})
