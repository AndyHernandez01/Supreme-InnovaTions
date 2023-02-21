from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    location: Optional[str] = None

class ItemCreate(ItemBase):
    location: str

class ItemUpdate(ItemBase):
    pass
