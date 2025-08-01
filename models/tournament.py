from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, date
from sqlalchemy.orm import relationship

from database.db import Base
from enums.tournament import TieBreakerRuleEnum

class Tournament(Base):
    
    __tablename__ = "tournaments"
    
    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String(150))
    start_date:date = Column(Date)
    end_date:date = Column(Date)
    winner_team_id:int =  Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    winner_team = relationship("Team")
    config = relationship("TournamentConfig", back_populates="tournament", uselist=False)
    groups = relationship("Group", back_populates="tournament")
    playoffs = relationship("Playoff", back_populates="tournament")
    awards = relationship("Award", back_populates="tournament")
    standings = relationship("TournamentStanding", back_populates="tournament")

class TournamentConfig(Base):
    
    __tablename__ = "tournament_configs"
    
    id:int = Column(Integer, primary_key=True)
    tournament_id:int = Column(Integer, ForeignKey("tournaments.id"))
    allow_draws:bool = Column(Boolean, default=True)
    points_win:int = Column(Integer, default=3)
    points_draw:int = Column(Integer, default=1)
    points_loss:int = Column(Integer, default=0)
    tie_break_rule:enumerate = Column(ENUM(TieBreakerRuleEnum, name="tiebreakruleenum", create_type=False), default=TieBreakerRuleEnum.GOAL_DIFFERENCE)
    group_size:int = Column(Integer, nullable=True)
    advance_teams_per_group:int = Column(Integer, nullable=True)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    tournament = relationship("Tournament", back_populates="config")

class TournamentStanding(Base):
    
    __tablename__ = "tournament_standings"
    
    id:int = Column(Integer, primary_key=True, index=True)
    tournament_id:int = Column(Integer, ForeignKey("tournaments.id"))
    team_id:int = Column(Integer, ForeignKey("teams.id"))
    played:int = Column(Integer, default=0)
    wins:int = Column(Integer, default=0)
    draws:int = Column(Integer, default=0)
    losses:int = Column(Integer, default=0)
    goals_for:int = Column(Integer, default=0)
    goals_againt:int = Column(Integer, default=0)
    goal_difference:int = Column(Integer, default=0)
    
    tournament = relationship("Tournament", back_populates="standings")
    team = relationship("Team")
