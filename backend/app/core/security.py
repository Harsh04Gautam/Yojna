from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()

ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hash: str) -> tuple[bool, str | None]:
    return password_hash.verify_and_update(password, hash)


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"exp": expire, "sub": str(subject)}
    token = jwt.encode(
        payload=payload, key=settings.SECRET_KEY, algorithm=ALGORITHM)
    return token
