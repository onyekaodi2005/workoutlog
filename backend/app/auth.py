from passlib.context import CryptContext
from jose import jwt
import os
from datetime import datetime, timedelta

pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET = os.getenv('SECRET_KEY', 'devsecret')
ALGO = 'HS256'

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

def create_token(email: str, minutes: int = 60):
    exp = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode({'sub': email, 'exp': exp}, SECRET, algorithm=ALGO)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get('sub')
    except Exception:
        return None
