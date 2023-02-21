from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from wds-api.db.base import Base

class Item(Base):
  wds_serial = Column(Integer, primary_key=True, index=True) 
  location = Column(String, index=True)
  #owner_id = Column(Integer, ForeignKey("user.id"))
  #owner = relationship("User", back_populates="items")
  time_created = Column(DateTime(timezone=True), server_default=func.now())
  last_updated = Column(DateTime(timezone=True), onupdate=func.now())
