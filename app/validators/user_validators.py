from fastapi import HTTPException, status

from app.models import User, UserConfig
from app.utils import api_utils, constants as const, message_utils as msg


def verify_password(user: User, password: str):
    if not user or not api_utils.verify_password(password, user.password):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = msg.get_message(msg.ME0001_INVALID_EMAIL_OR_PASSWORD)
        )

def ensure_not_deleted(user: User):
    if user.dele_flg == "T":
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = msg.get_message(msg.ME0010_ACCOUNT_ALREADY_DELETED)
        )

def ensure_deleted(user: User):
    if not user.dele_flg == "T":
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = msg.get_message(msg.MW0002_USER_ALREADY_EXISTS)
        )

def ensure_activate(user_config: UserConfig):
    if not user_config or not user_config.val == "T":
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = msg.get_message(msg.ME0009_ACCOUNT_NOT_ACTIVATE)
        )

def ensure_alive_token(user: User):
    if not user:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, 
            detail = msg.get_message(msg.ME0003_SESSION_TIME_OUT)
        )

def exist_account(user: User):
    if not user:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail = msg.get_message(msg.ME0004_ACCOUNT_NOT_EXISTS)
        )
