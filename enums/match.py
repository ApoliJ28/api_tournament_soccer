from enum import Enum as PyEnum

class StatusMatchEnum(str, PyEnum):
    PLANNED:str = "planned"
    ONGOING:str = "ongoing"
    FINISHED:str = "finished"
