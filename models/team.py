from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
from sqlalchemy.orm import relationship

from database.db import Base
from enums.player import PlayerPositonFutsalEnum

class Team(Base):
    
    __tablename__ = "teams"
    
    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String(150), unique=True)
    short_name:str = Column(String(20), unique=True)
    logo_url:str = Column(String(500), nullable=True)
    coach_id:int = Column(Integer, ForeignKey("coachs.id"), nullable=True)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    players = relationship("Player", back_populates="team")
    coach = relationship("Coach", back_populates="team", uselist=False)
    team_lineups = relationship("TeamLineup", back_populates="team")

# TeamLineupFutsal: alineación general del equipo FUTSAL

class TeamLineup(Base):
    
    __tablename__ = "team_lineups"
    
    id:int = Column(Integer, primary_key=True)
    team_id:int = Column(Integer, ForeignKey("teams.id"))
    player_id:int = Column(Integer, ForeignKey("players.id"))
    position:enumerate = Column(ENUM(PlayerPositonFutsalEnum, name="playerpositionfutsalenum", create_type=False))
    is_starter:bool = Column(Boolean, default=True) #Titular o suplente
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    team = relationship("Team", back_populates="team_lineups")
    player = relationship("Player")
