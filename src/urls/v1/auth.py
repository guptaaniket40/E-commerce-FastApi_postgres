from fastapi import APIRouter

from src.services.auth.controller import AuthController
from src.services.auth.serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    RefreshTokenSerializer
)

router= APIRouter(prefix="/auth",tags=["Auth"]
)


@router.post("/signup")
async def signup(
    request: UserSignupSerializer
):
    return await AuthController.signup(
        user_data=request
    )


@router.post("/login")
async def login(
    request: UserLoginSerializer
):
    return await AuthController.login(
        user_data=request
    )


@router.post("/refresh-token")
async def refresh_token(
    request: RefreshTokenSerializer
):
    return await AuthController.refresh_token(
          user_data=request
    )