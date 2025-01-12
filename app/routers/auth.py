# app/routers/auth.py
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.database import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User

# Klucz do podpisywania tokenów (np. SECRET_KEY = os.environ["SECRET_KEY"])
SECRET_KEY = "SECRET_JWT_KEY_123456"  # w praktyce trzymany w .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # na ile minut wystawiamy token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generuje JWT z danymi (np. sub=login)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Sprawdź, czy taki login już istnieje
    existing_user = db.query(User).filter(User.login == user_data.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already in use")
    
    # Hashujemy hasło
    hashed_pw = hash_password(user_data.password)
    
    new_user = User(
        login=user_data.login,
        hashed_password=hashed_pw,
        name=user_data.name,
        height=user_data.height,
        weight=user_data.weight,
        birth_date=user_data.birth_date,
        score=user_data.score
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Zwraca obiekt usera na podstawie przekazanego tokenu."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login: str = payload.get("sub")
        if user_login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.login == user_login).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Zwraca token JWT, jeśli login i hasło prawidłowe."""
    user = db.query(User).filter(User.login == login_data.login).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid login or password")
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid login or password")
    
    # Login i hasło prawidłowe – generujemy token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login, "uuid": user.uuid},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
