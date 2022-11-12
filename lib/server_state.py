from typing import List, Dict

from protocol0.domain.lom.device.DeviceEnum import DeviceEnum
from protocol0.domain.lom.sample.SampleCategoryEnum import SampleCategoryEnum
from pydantic import BaseModel

from lib.ableton_set import AbletonSet, AbletonSetManager


class ServerState(BaseModel):
    sets: List[AbletonSet]
    set_shortcuts: List[str]
    sample_categories: Dict[str, List[str]]
    favorite_device_names: List[List[str]]
    insert_favorite_device_names: List[str]

    @classmethod
    def create(cls) -> "ServerState":
        sets = list(sorted([ss.dict() for ss in AbletonSetManager.all()], key=lambda s: s["title"]))

        return ServerState(
            sets=sets,
            set_shortcuts=["last", "default", "new"],
            sample_categories={
                category.name.lower(): category.subcategories
                for category in list(SampleCategoryEnum)
            },
            favorite_device_names=[
                [device.name for device in row] for row in DeviceEnum.favorites()
            ],
            insert_favorite_device_names=[device.name for device in DeviceEnum.insert_favorites()],
        )
