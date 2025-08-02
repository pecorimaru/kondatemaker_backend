from fastapi import HTTPException, status
from app.models import User, UserConfig
from app.utils import api_utils, constants as const, message_utils as msg


def check_weekday_cd(weekday_cd: str):
    """曜日コードチェック"""
    if weekday_cd == const.EMPTY_CD:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0016_NOT_SELECTED_ITEM, "曜日"),
        )


def verify_password(user: User, password: str):
    """パスワード検証"""
    if not user or not api_utils.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=msg.get_message(msg.ME0001_INVALID_EMAIL_OR_PASSWORD)
        )


def ensure_not_deleted(user: User):
    """削除状態でないことを確認"""
    if user.dele_flg == "T":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=msg.get_message(msg.ME0010_ACCOUNT_ALREADY_DELETED)
        )


def ensure_deleted(user: User):
    """削除状態であることを確認"""
    if not user.dele_flg == "T":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=msg.get_message(msg.MW0002_USER_ALREADY_EXISTS)
        )


def ensure_activate(user_config: UserConfig):
    """アクティベート状態確認"""
    if not user_config or not user_config.val == "T":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=msg.get_message(msg.ME0009_ACCOUNT_NOT_ACTIVATE)
        )


def ensure_alive_token(user: User):
    """トークン有効性確認"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=msg.get_message(msg.ME0003_SESSION_TIME_OUT)
        ) 