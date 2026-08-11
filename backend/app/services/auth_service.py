from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token
)
from app.auth.jwt_handler import verify_token


class AuthService:

    @staticmethod
    def register(db: Session, data):

        existing_user = UserRepository.get_by_email(
            db,
            data.email
        )

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role
        )

        return UserRepository.create(db, user)

    @staticmethod
    def login(db: Session, data):

        user = UserRepository.get_by_email(
            db,
            data.email
        )

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(
            data.password,
            user.password
        ):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value
            }
        )

        refresh_token = create_refresh_token(   
            {
                "sub": str(user.id),
                "role": user.role.value
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    @staticmethod
    def refresh_access_token(refresh_token: str):

        payload = verify_token(refresh_token)

        if payload is None:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        access_token = create_access_token(
            {
                "sub": payload["sub"],
                "role": payload.get("role")
            }
        )

        return {
            "access_token": access_token
        }
    @staticmethod
    def reset_password(
        db: Session,
        email: str,
        new_password: str
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if user is None:
            raise ValueError("User not found")

        hashed_password = hash_password(new_password)

        UserRepository.update_password(
            db,
            user,
            hashed_password
        )

        return {
            "message": "Password reset successfully"
        }