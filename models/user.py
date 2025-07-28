from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class RoleUserEnum(str, Enum):
    ADMIN:str = "admin" # Administrador del Sistema
    COACH:str = "coach" # Coach del Equipo
    PLAYER:str = "player" # Jugador
    GUEST:str = "guest" # Visita
    CONFIGURATOR:str = "configurator" # Para torneo/partido creacion edicion y asi

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    
    id:int = Column(Integer, primary_key=True, index=True)
    username:str = Column(String, unique=True, index=True)
    email:str = Column(String, unique=True, index=True)
    dni:str = Column(String, unique=True, index=True)
    first_name:str = Column(String)
    last_name:str = Column(String)
    password:str = Column(String)
    is_active:bool = Column(Boolean, default=True)
    role:enumerate = Column(Enum(RoleUserEnum), default=RoleUserEnum.GUEST)
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    updated_datetime:datetime = Column(DateTime, default=datetime.now, onupdate=datetime.now)
