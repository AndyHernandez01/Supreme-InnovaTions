from typing import List
 
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from wds-api.crud.base import CRUDBase
from wds-api.models.item import Item
from wds-api.schemas.item import ItemCreate, ItemUpdate

