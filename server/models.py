from typing import Optional

from pydantic import BaseModel


class Search():
    LAST_SEARCH = None


class Action(BaseModel):
    name: Optional[str] = None
    arg: Optional[str] = None
