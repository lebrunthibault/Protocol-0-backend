from typing import List, Dict, Union

from protocol0.domain.lom.device.DeviceEnum import DeviceEnum
from protocol0.domain.lom.device.DeviceEnumGroup import DeviceEnumGroup
from protocol0.domain.lom.sample.SampleCategoryEnum import SampleCategoryEnum
from pydantic import BaseModel

from lib.ableton_set import AbletonSet, AbletonSetManager


class ServerState(BaseModel):
    sets: List[AbletonSet]
    set_shortcuts: List[str]
    sample_categories: Dict[str, List[str]]
    favorite_device_names: List[List[Union[str, Dict]]]
    insert_favorite_device_names: List[str]

    @classmethod
    def create(cls) -> "ServerState":
        sets = list(sorted([ss.dict() for ss in AbletonSetManager.all()], key=lambda s: s["title"]))
        favorite_device_names = []

        def serialize_device_enum(d):
            # type: (Union[DeviceEnum, DeviceEnumGroup]) -> Union[str, Dict]
            if isinstance(d, DeviceEnum):
                return d.name
            else:
                return d.to_dict()

        from loguru import logger
        logger.success(DeviceEnum.favorites())
        return ServerState(
            sets=sets,
            set_shortcuts=["last", "default", "new"],
            sample_categories={
                category.name.lower(): category.subcategories
                for category in list(SampleCategoryEnum)
            },
            favorite_device_names=[
                list(map(serialize_device_enum, row)) for row in DeviceEnum.favorites()
            ],
            insert_favorite_device_names=[device.name for device in DeviceEnum.insert_favorites()],
        )
