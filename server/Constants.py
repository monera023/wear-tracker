from enum import Enum
from typing import Optional

from pydantic import BaseModel


class WearType(Enum):
    Shirt_Tees = 0
    Pants_shorts_pj = 1
    Jackets = 2


class DbConstants:
    WEAR_ITEM = "wear_items"
    WEAR_ITEM_TRACKING = "wear_item_tracking"


class WearItem(BaseModel):
    id: Optional[int] = -1
    name: str
    type: WearType
    active: bool
    color: str
    comment: str

class WearItemTrackingEntry(BaseModel):
    item_id: int
    counter: int
    date: str

class WearItemTrackingSumEntity(BaseModel):
    item_id: int
    name: str
    type: str
    active: bool
    total: int
