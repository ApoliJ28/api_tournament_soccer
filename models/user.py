from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

from database.db import Base

from enums.user import RoleUserEnum

class User(Base):
    __tablename__ = "users"
    
    id:int = Column(Integer, primary_key=True, index=True)
    username:str = Column(String, unique=True, index=True)
    email:str = Column(String, unique=True, index=True)
    dni:str = Column(String, unique=True, index=True)
    first_name:str = Column(String)
    last_name:str = Column(String)
    password:str = Column(String)
    is_active:bool = Column(Boolean, default=True)
    role:enumerate = Column(ENUM(RoleUserEnum, name="roleuserenum", create_type=False), default=RoleUserEnum.GUEST)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
