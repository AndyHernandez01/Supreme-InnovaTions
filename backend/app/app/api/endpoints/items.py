from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/")
def read(
        db: Session = Depends(deps.get_db),
        skip: int = 0, #Where are we starting in the table
        limit: int = 100, #How many values are we outputting
        search: str = '',
        )-> Any:

    #Retrieving items
    items = crud.wds.get_multi(db, skip=skip, search=search, limit=limit)
    

    return items
@router.get("/loc")
def read_loc(
        db: Session = Depends(deps.get_db)
        ):
        location = crud.wds.get_all_locations(db)
        return location
@router.post("/", response_model=schemas.Item)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ItemCreate,
        wds_serial: str
        )->Any:
    item = crud.wds.create_by_wds(db, obj_in=item_in, wds_serial=wds_serial)
    return item
    
@router.put("/{wds_serial}", response_model=schemas.Item)
def update_item(        
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ItemCreate,
        wds_serial: str
        )->Any:
    #Gets DB entry, then updates
    item = crud.wds.get(db=db, id=wds_serial)
    item = crud.wds.update(db=db,db_obj=item, obj_in=item_in)
    return item
@router.delete("/{wds_serial}", response_model=schemas.Item)
def delete_item(
  *,
  db: Session = Depends(deps.get_db),
  wds_serial: int,
)->Any:
    item = crud.wds.get(db=db, id=wds_serial)
    if not item:
      raise HTTPException(status_code=404, detail="Item not found")
    item = crud.wds.remove(db=db,id=wds_serial)
    return item
