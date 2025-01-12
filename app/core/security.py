# app/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Zwraca zahashowane hasło (bcrypt)."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Weryfikuje podane hasło (plaintext) z hashem w bazie."""
    return pwd_context.verify(plain_password, hashed_password)
