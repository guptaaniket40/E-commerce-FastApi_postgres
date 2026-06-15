from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db
from src.services.auth.controller import AuthController
from src.services.auth.serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    RefreshTokenSerializer
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(request: UserSignupSerializer, db: AsyncSession = Depends(get_db)):
    return await AuthController.signup(user_data=request, db=db)


@router.post("/login")
async def login(request: UserLoginSerializer, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(user_data=request, db=db)


@router.post("/refresh-token")
async def refresh_token(request: RefreshTokenSerializer):
    return await AuthController.refresh_token(user_data=request)