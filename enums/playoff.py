from enum import Enum as PyEnum

class TypePlayOffsEnum(str, PyEnum):
    ROUND_OF_32:str = "round_of_32"
    ROUND_OF_16:str = "round_of_16"
    QUARTER_FINALS:str = "quarter_finals"
    SEMI_FINALS:str = "semi_finals"
    FINAL:str = "final"
