from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import Settings

setting = Settings()

engine = create_engine(setting.database_url)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()
