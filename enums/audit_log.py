from enum import Enum as PyEnum

class ActionAuditLogEnum(str, PyEnum):
    UPDATE:str = "update"
    CREATE:str = "create"
    DELETE:str = "delete"
    START_MATCH:str = "start_match"
    ACTION_MATCH_EVENT:str = "action_match_even"
