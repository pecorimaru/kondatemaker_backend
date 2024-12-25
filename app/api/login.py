from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from typing import Optional

from app.core.session import get_db
from app.utils.api_utils import CamelModel, decode_token
from app.services import LoginService
from app.utils import message_utils as msg 


router = APIRouter()


class LoginRequest(CamelModel):
    email: str
    password: Optional[str]=None

class LoginResponse(CamelModel):
    status_code: int
    message: str
    user_nm: Optional[str]=None
    access_token: Optional[str]=None

class VerifyRequest(CamelModel):
    token: str

class VerifyResponse(CamelModel):
    status_code: int

class RefreshRequest(CamelModel):
    refresh_token: str

class RefreshResponse(CamelModel):
    status_code: int
    new_access_token: str

class ResetPasswordRequest(CamelModel):
    email: str

class ResetPasswordResponse(CamelModel):
    status_code: int
    message: str

class CreateUserRequest(CamelModel):
    email: str
    password: str

class CreateUserResponse(CamelModel):
    status_code: int
    message: str

class ActivateRequest(CamelModel):
    token: str

class ActivateResponse(CamelModel):
    status_code: int
    message: str


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):

    login_service = LoginService(None, None, None, db)
    token_data = login_service.login(request.email, request.password)

    # クッキーにリフレッシュトークンをセット
    response.set_cookie(
        key="refresh_token",
        value=token_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7日間
    )

    return LoginResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0001_LOGIN_SUCCESSFUL),
        access_token = token_data.access_token,
    )


@router.post("/googleLogin", response_model=LoginResponse)
def google_login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):

    # Google のトークンを検証
    login_service = LoginService(None, None, None, db)
    token_data = login_service.google_login(request.email)

    # クッキーにリフレッシュトークンをセット
    response.set_cookie(
        key="refresh_token",
        value=token_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7日間
    )

    return LoginResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0001_LOGIN_SUCCESSFUL),
        access_token = token_data.access_token,
    )

    

@router.post("/verify", response_model=VerifyResponse)
def verify(request: VerifyRequest):
    decode_token(request.token)

    return VerifyResponse(
        status_code = status.HTTP_200_OK,
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(request: Request, db: Session = Depends(get_db)):

    refresh_token = request.cookies.get("refresh_token")

    login_service = LoginService(None, None, None, db)
    new_access_token = login_service.refresh_access_token(refresh_token)

    return RefreshResponse(
        status_code = status.HTTP_200_OK,
        new_access_token = new_access_token,
    )


@router.post("/resetPassword", response_model=ResetPasswordResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):

    login_service = LoginService(None, None, None, db)
    login_service.reset_password(request.email)

    return ResetPasswordResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0004_RESET_PASSWORD_DONE),
    )


@router.post("/createUser", response_model=CreateUserResponse)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):

    login_service = LoginService(None, None, None, db)
    login_service.create_user(request.email, request.password)

    return CreateUserResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0005_CREATE_USER_DONE),
    )


@router.post("/activate", response_model=ActivateResponse)
def activate_user(request: ActivateRequest, db: Session = Depends(get_db)):

    login_service = LoginService(None, None, None, db)
    login_service.activate_user(request.token)

    return ActivateResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0006_ACTIVATE_USER_DONE),
    )