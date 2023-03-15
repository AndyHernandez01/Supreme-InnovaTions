from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    location: Optional[str] = None

class ItemCreate(ItemBase):
    location: str

class ItemUpdate(ItemBase):
    pass

class ItemInDB(ItemBase):
    wds_serial: int
    location: str
    class Config:
        orm_mode = True

class Item(ItemInDB):
    pass
