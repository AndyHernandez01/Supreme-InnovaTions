from typing import List
 
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )
    def create_by_wds(
      self, db: Session, *, obj_in: ItemCreate, wds_serial:int
    )-> Item:
      obj_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_data, wds_serial=wds_serial)
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj




wds = CRUDItem(Item)
