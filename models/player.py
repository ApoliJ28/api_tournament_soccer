from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, Date, ForeignKey
from datetime import datetime, date
from sqlalchemy.orm import relationship

from database.db import Base
from enums.player import PlayerPositonFutsalEnum

class Player(Base):
    
    __tablename__ = "players"
    
    id:int = Column(Integer, primary_key=True, index=True)
    first_name:str = Column(String(150))
    last_name:str = Column(String(150))
    dni:str = Column(String(30), unique=True, Index=True)
    photo_url:str = Column(String(500), nullable=True)
    birth_date:date = Column(Date)
    position:enumerate = Column(SqlEnum(PlayerPositonFutsalEnum), default=PlayerPositonFutsalEnum.FB)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")
