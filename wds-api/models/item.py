from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from wds-api.db.base import Base

class Item(Base):
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  owner_id = Column(Integer, ForeignKey("user.id")
  owner = relationship("User", back_populates="items")
  