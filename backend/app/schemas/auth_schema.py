from pydantic import BaseModel
from pydantic import EmailStr

from app.models.enums import UserRole


class UserRegister(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    role: UserRole


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str