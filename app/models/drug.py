# app/models/drug.py
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_uuid = Column(String, ForeignKey("users.uuid"), index=True, nullable=False)

    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)
    additional_info = Column(String, nullable=True)

    times = Column(Text, nullable=True)

    is_notification_enabled = Column(Boolean, default=False)
