from typing import List
 
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_multi(
        self, db: Session, *, search: str = '', skip: int = 0, limit: int = 100
    ) -> List[Item]:
        if search != '':
            return (
                db.query(self.model).filter(Item.location==search)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .offset(skip)
                .limit(limit)
                .all()
            )
    def create_by_wds(
      self, db: Session, *, obj_in: ItemCreate, wds_serial:str
    )-> Item:
      obj_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_data, wds_serial=wds_serial)
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

    def get_all_locations(
        self, db: Session
        ):
        return db.query(Item.location).all()

wds = CRUDItem(Item)
