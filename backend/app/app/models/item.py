from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from savage.models import SavageLogMixin, SavageModelMixin
from app.db.base import Base

class Item(Base, SavageModelMixin):
  version_columns = ['wds_serial']
  #__table_args__= (UniqueConstraint('wds_serial'),)
  """,'func_status','accum_sys_time','accum_standby','location'"""
  wds_serial = Column(String, primary_key=True)  #Collected from WDS data
  func_status = Column(String, index=True)
  accum_sys_time = Column(Integer, index=True)
  accum_standby = Column(Integer, index=True)
  location = Column(String, index=True)
  time_created = Column(DateTime(timezone=True), default=func.now())
  last_updated = Column(DateTime(timezone=True), onupdate=func.now())

class ItemHistory(Base,SavageLogMixin):
  __table_args__ = (
    UniqueConstraint('wds_serial', 'version_id'),
  )
  """,'func_status','accum_sys_time','accum_standby','location',"""
  user_id = Column(Integer)
  wds_serial = Column(String)
  #func_status = Column(String, index=True)
  #accum_sys_time = Column(Integer, index=True)
  #accum_standby = Column(Integer, index=True)
  #location = Column(String, index=True)
  #hist = Column(DateTime(timezone=True), default=func.now())
  #ForeignKeyConstraint(['wds_serial','func_state','accum_sys_time','accum_standby','location'], 
                      #['item.wds_serial','item.func_state','item.accum_sys_time','item.accum_standby','item.location'])
  #item = relationship("Item", back_populates="itemhistory")


