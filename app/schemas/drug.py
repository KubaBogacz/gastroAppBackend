# app/schemas/drug.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DrugBase(BaseModel):
    name: str
    dosage: str
    date_from: datetime
    date_to: datetime
    additional_info: str
    times: str
    is_notification_enabled: bool

class DrugCreate(DrugBase):
    """Schemat do tworzenia nowego leku (POST)."""
    user_uuid: str

class DrugUpdate(BaseModel):
    """Schemat do aktualizacji leku (PATCH). 
       Wszystkie pola opcjonalne - aktualizujemy tylko to, co się zmienia."""
    name: Optional[str] = None
    dosage: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    additional_info: Optional[str] = None
    times: Optional[str] = None
    is_notification_enabled: Optional[bool] = None

class DrugOut(DrugBase):
    """Schemat zwracany w odpowiedzi."""
    id: str
    user_uuid: str

    class Config:
        orm_mode = True
