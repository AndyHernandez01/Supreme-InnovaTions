from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase():
  def __init__(self, model: Type[ModelType]):
    """
    CRUD Defaults (create,read,update,delete)
    model: SQLalchemy modelclass;
    schema: Pydantic model
    """
    
    self.model = model
    
  #Returns all data from database with inputed ID
  def get(self, db: Session, id: Any) -> Optional[ModelType]: 
    return db.query(self.model).filter(self.model.id == id).all()
  
  #Gets multiple tables from the databse.
  def get_multi(self, db: Session, *, skip: int=0, limit: int = 100) -> List[ModelType]:
    return db.query(self.model).offset(skip).limit(limit).all()
    
  def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    #Encodes any data into JSON encoding, so database can be updated with that info
    obj_in_data = jsonable_encoder(obj_in) 
    db_obj = self.model(**obj_in_data) #sets data to model
    db.add(db_obj)  #adds to database
    db.commit()  #commits new info to database
    db.refresh(db_obj) 
    return db_obj
  def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str,Any]]) -> ModelType
    #Encodes any data into JSON encoding, so database can be updated with that info
    obj_data = jsonable_encoder(db_obj) 
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
  def remove(self, db: Session, *, id: int) -> ModelType:
    obj = db.query(self.model).get(id)
    db.delete(obj)
    db.commit()
    return obj
    
    