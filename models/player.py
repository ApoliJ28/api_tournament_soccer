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
    team_id:int = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")

class PlayerStats(Base):
    
    __tablename__ = "player_stats"
    
    id:int = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    match_id = Column(Integer, ForeignKey("matches.id"))
    goals = Column(Integer, default=0)
    assist = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    
    player = relationship("Player", back_populates="stats")
    match = relationship("Match", back_populates="player_stats")

class PlayerAward(Base):
    __tablename__ = "player_awards"

    id:int = Column(Integer, primary_key=True, index=True)
    player_id:int = Column(Integer, ForeignKey("players.id"))
    award_id:int = Column(Integer, ForeignKey("awards.id"))
    date_awarded:datetime = Column(DateTime, default=datetime.now)

    player = relationship("Player")
    award = relationship("Award", back_populates="player_awards")
