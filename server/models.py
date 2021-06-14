from typing import Optional

from a_protocol_0.enums.ServerActionEnum import ServerActionEnum
from pydantic import BaseModel


class Search():
    LAST_SEARCH = None


class Action(BaseModel):
    enum: Optional[ServerActionEnum] = None
    arg: Optional[str] = None

    @property
    def enum_val(self):
        return ServerActionEnum.get_from_value(self.enum)
