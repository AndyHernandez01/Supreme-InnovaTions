from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    func_status: str
    accum_sys_time: int
    accum_standby: int
    location: str

class ItemCreate(ItemBase):
    func_status: str
    accum_sys_time: int
    accum_standby: int
    location: str

class ItemUpdate(ItemBase):
    pass

class ItemInDB(ItemBase):
    func_status: str
    accum_sys_time: int
    accum_standby: int
    location: str
    class Config:
        orm_mode = True

class Item(ItemInDB):
    pass
