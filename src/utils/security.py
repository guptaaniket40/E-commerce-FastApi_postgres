from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db
from src.database.models import User
from src.database.jwt_config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

 
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

 
bearer_scheme = HTTPBearer()


 
class TokenHandler:

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        payload = data.copy()

        payload.update({
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access"
        })

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        payload = data.copy()

        payload.update({
            "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh"
        })

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def decode_token(cls, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )


 
class PasswordHasher:

    @classmethod
    def encrypt_password(cls, password: str) -> str:
        return PWD_CONTEXT.hash(password)

    @classmethod
    def check_password(cls, plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)


 
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials
    payload = TokenHandler.decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user