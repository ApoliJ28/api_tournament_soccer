from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

class Group(Base):
    __tablename__ = "groups"

    id:int = Column(Integer, primary_key=True)
    tournament_id:int = Column(Integer, ForeignKey("tournaments.id"))
    name:str = Column(String(50))

    tournament = relationship("Tournament", back_populates="groups")
    stagings = relationship("GroupStanding", back_populates="group")
    matches = relationship("Match", back_populates="group")

class GroupStanding(Base):
    
    __tablename__ = "group_standings"
    
    id:int = Column(Integer, primary_key=True, index=True)
    group_id:int = Column(Integer, ForeignKey("groups.id"))
    team_id:int = Column(Integer, ForeignKey("teams.id"))
    points:int = Column(Integer, default=0)
    played:int = Column(Integer, default=0)
    wins:int = Column(Integer, default=0)
    draws:int = Column(Integer, default=0)
    losses:int = Column(Integer, default=0)
    goals_for:int = Column(Integer, default=0)
    goals_againt:int = Column(Integer, default=0)
    goal_difference:int = Column(Integer, default=0)
    
    group = relationship("Group", back_populates="standings")
    team = relationship("Team")
