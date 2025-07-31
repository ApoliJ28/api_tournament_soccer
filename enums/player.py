from enum import Enum as PyEnum

class PlayerPositonFutsalEnum(str, PyEnum):
    GK:str = "gk"
    FB:str = "fb"
    W:str = "w"
    FW:str = "fw"
    P:str = "p"
