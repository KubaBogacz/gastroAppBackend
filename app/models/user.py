# app/models/user.py
import uuid
from sqlalchemy import Column, String, Float, Date
from app.database import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    name = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    birth_date = Column(Date, nullable=False)
    score = Column(Float, default=0.0)
