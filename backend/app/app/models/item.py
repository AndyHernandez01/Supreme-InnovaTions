from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class Item(Base):
  wds_serial = Column(String, primary_key=True, index=True)  #Collected from WDS data
  func_status = Column(String, index=True)
  accum_sys_time = Column(Integer, index=True)
  accum_standby = Column(Integer, index=True)
  location = Column(String, index=True)
  time_created = Column(DateTime(timezone=True), default=func.now())
  last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
