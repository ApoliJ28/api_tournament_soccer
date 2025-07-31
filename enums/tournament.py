from enum import Enum as PyEnum

class TieBreakerRuleEnum(str, PyEnum):
    GOAL_DIFFERENCE:str = "goal_difference"
    HEAD_TO_HEAD:str = "head_to_head"
    GOALS_SCORED:str = "goals_scored"
