from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from database.db import Base
from enums.award import AwardTypeEnum

class Award(Base):
    
    __tablename__ = "awards"
    
    id:int = Column(Integer, primary_key=True, index=True)
    tournament_id:int = Column(Integer, ForeignKey("tournaments.id"))
    name:enumerate = Column(ENUM(AwardTypeEnum, name="awardtypeenum", create_type=False))
    description:str = Column(String(255), nullable=True)

    tournament = relationship("Tournament", back_populates="awards")
    player_awards = relationship("PlayerAward", back_populates="award")
