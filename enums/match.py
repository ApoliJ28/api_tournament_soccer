from enum import Enum as PyEnum

class StatusMatchEnum(str, PyEnum):
    PLANNED:str = "planned"
    ONGOING:str = "ongoing"
    FINISHED:str = "finished"

class MatchEventTypeEnum(str, PyEnum):
    GOAL = "goal"
    ASSIST = "assist"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"
    SUBSTITUTION_IN = "substitution_in"
    SUBSTITUTION_OUT = "substitution_out"