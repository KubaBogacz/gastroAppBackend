# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # wymaga autoryzacji
):
    """Zwraca listę wszystkich użytkowników, tylko jeśli jesteś zalogowany."""
    users = db.query(User).all()
    return users

@router.get("/{user_uuid}", response_model=UserOut)
def get_user(
    user_uuid: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Zwraca konkretnego usera po uuid, tylko dla zalogowanych."""
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/bylogin/{login}", response_model=UserOut)
def get_user_by_login(
    login: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_uuid}", response_model=UserOut)
def update_user(
    user_uuid: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(data)
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # tylko uaktualniamy, co przychodzi
    if data.score is not None:
        user.score = data.score
    if data.is_onboarded is not None:
        user.is_onboarded = data.is_onboarded
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_uuid: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Usuwa użytkownika, tylko dla zalogowanych."""
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return
