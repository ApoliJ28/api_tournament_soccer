from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, Date, ForeignKey
from datetime import datetime, date as dt
from sqlalchemy.orm import relationship

from database.db import Base
from enums.match import StatusMatchEnum, MatchEventTypeEnum

class Match(Base):
    
    __tablename__ = "matches"
    
    id:int = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    playoff_id = Column(Integer, ForeignKey("playoffs.id"), nullable=True)
    date:dt = Column(Date)
    home_team_id:int = Column(Integer, ForeignKey("teams.id"), nullable=True)
    away_team_id:int = Column(Integer, ForeignKey("teams.id"), nullable=True)
    home_team_score:int = Column(Integer, default=0)
    away_team_score:int = Column(Integer, default=0)
    status:enumerate = Column(SqlEnum(StatusMatchEnum), default=StatusMatchEnum.PLANNED)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    group = relationship("Group", back_populates="matches")
    playoff = relationship("Playoff", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    events = relationship("MatchEvent", back_populates="match")
    player_stats = relationship("PlayerStats", back_populates="match")
    team_lineups = relationship("MatchTeamLineup", back_populates="match")

class MatchEvent(Base):
    
    __tablename__ = "match_events"
    
    id:int = Column(Integer, primary_key=True, index=True)
    match_id:int = Column(Integer, ForeignKey("matches.id"))
    player_id:int = Column(Integer, ForeignKey("players.id"))
    event_type:enumerate = Column(SqlEnum(MatchEventTypeEnum))
    minute:int = Column(Integer)
    description:str = Column(String(255), nullable=True)
    
    match = relationship("Match", back_populates="events")
    player = relationship("Player")
