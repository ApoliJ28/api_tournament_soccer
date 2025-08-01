from sqlalchemy import Column, Integer, String, DateTime, Date
from datetime import datetime, date
from sqlalchemy.orm import relationship

from database.db import Base

class Coach(Base):
    
    __tablename__ = "coachs"
    
    id:int = Column(Integer, primary_key=True, index=True)
    first_name:str = Column(String(150))
    last_name:str = Column(String(150))
    dni:str = Column(String(30), unique=True, index=True)
    photo_url:str = Column(String(500), nullable=True)
    birth_date:date = Column(Date)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    team = relationship("Team", back_populates="coach")
