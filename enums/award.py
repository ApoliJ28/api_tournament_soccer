from enum import Enum as PyEnum

class AwardTypeEnum(str, PyEnum):
    MVP:str = "mvp"
    BEST_GOALKEEPER:str = "best_goalkeeper"
    TOP_SCORER:str = "top_scorer"
    FAIR_PLAY:str = "fair_play"
