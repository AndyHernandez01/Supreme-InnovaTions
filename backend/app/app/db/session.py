from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
#Creates Postgress session
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
