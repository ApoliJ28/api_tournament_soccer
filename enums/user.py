from enum import Enum as PyEnum

class RoleUserEnum(str, PyEnum):
    ADMIN:str = "admin" # Administrador del Sistema
    COACH:str = "coach" # Coach del Equipo
    PLAYER:str = "player" # Jugador
    GUEST:str = "guest" # Visita
    CONFIGURATOR:str = "configurator" # Para torneo/partido creacion edicion y asi
