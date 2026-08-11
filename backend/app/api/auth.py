from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse
)
from app.services.auth_service import AuthService
from app.schemas.auth_schema import (
    RefreshTokenRequest,
    AccessTokenResponse
)
from app.schemas.auth_schema import ResetPasswordRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    try:

        created_user = AuthService.register(
            db,
            user
        )

        return {
            "message": "User registered successfully",
            "user_id": str(created_user.id)
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):

    try:

        return AuthService.login(
            db,
            credentials
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.post(
    "/refresh",
    response_model=AccessTokenResponse
)
def refresh_token(
    request: RefreshTokenRequest
):

    try:

        return AuthService.refresh_access_token(
            request.refresh_token
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    try:

        return AuthService.reset_password(
            db,
            request.email,
            request.new_password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )