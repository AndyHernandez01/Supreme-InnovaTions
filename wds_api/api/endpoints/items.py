from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from api import deps

router = APIRouter()

@router.get("/")
def read(
        db: Session = Depends(deps.get_db),
        skip: int = 0, #Where are we starting in the table
        limit: int = 100, #How many values are we outputting
        )-> Any:

    #Retrieving items
    items = crud.wds.get_multi(db, skip=skip, limit=limit)
    

    return items

@router.post("/", response_model=schemas.Item)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ItemCreate,
        wds_serial: int
        )->Any:
    item = crud.wds.create_by_wds(db, obj_in=item_in, wds_serial=wds_serial)
    return item
