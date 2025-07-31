from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from datetime import datetime
from sqlalchemy.orm import relationship

from database.db import Base
from enums.audit_log import ActionAuditLogEnum

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id:str = Column(Integer, primary_key=True)
    user_id:str = Column(Integer, ForeignKey("users.id"), nullable=True)
    action:str = Column(SqlEnum(ActionAuditLogEnum))
    model:str = Column(String(100))
    created_datetime:datetime = Column(DateTime, default=datetime.now)
    details:str = Column(String(1024), nullable=True)

    user = relationship("User")
