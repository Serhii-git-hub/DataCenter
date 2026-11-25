from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from core.config import settings

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)

def create_access_token(user_id: int, role: str) -> str:
    expire_date = datetime.now(timezone.utc) + timedelta(minutes = settings.auth_config.access_token_expire_minutes)
    payload = {'sub': str(user_id), 'role': role, 'exp': expire_date}
    return jwt.encode(payload,  settings.auth_config.secret_key,  algorithm=settings.auth_config.algorithm)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.auth_config.secret_key, algorithms=[settings.auth_config.algorithm])

