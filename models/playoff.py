from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from database.db import Base
from enums.playoff import TypePlayOffsEnum

class Playoff(Base):
    
    __tablename__ = "playoffs"
    
    id:int = Column(Integer, primary_key=True, index=True)
    tournament_id:int = Column(Integer, ForeignKey("tournaments.id"))
    round_name = Column(ENUM(TypePlayOffsEnum, name="typeplayoffenum", create_type=False), default=TypePlayOffsEnum.ROUND_OF_32)
    
    tournament = relationship("Tournament", back_populates="playoffs")
    matches = relationship("Match", back_populates="playoff")
