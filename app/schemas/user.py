# app/schemas/user.py
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    name: str
    height: float
    weight: float
    birth_date: date
    score: float = 0.0
    is_onboarded: bool = False

class UserCreate(UserBase):
    """Schemat używany przy rejestracji nowego użytkownika."""
    login: str
    password: str  # plaintext, w bazie i tak zapiszemy zhashowane

class UserLogin(BaseModel):
    """Schemat do logowania (login + hasło)."""
    login: str
    password: str

class UserUpdate(BaseModel):
    """Schemat używany przy np. aktualizacji score."""
    is_onboarded: bool = None
    score: float = None

class UserOut(UserBase):
    uuid: str
    
    class Config:
        orm_mode = True
