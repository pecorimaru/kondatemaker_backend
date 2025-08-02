from fastapi import HTTPException, status

import secrets, string, os
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from app.utils import message_utils as msg

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
secret_key =  os.getenv("SECRET_KEY")
algorithm =  os.getenv("ALGORITHM")


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class LoginInfo(CamelModel):
    user_id: Optional[int]=None
    group_id: Optional[int]=None
    owner_user_id: Optional[int]=None

class TokenData(CamelModel):
    access_token: str
    refresh_token: str


def to_camel_case(string):
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def convert_dict_to_camel_case(d):
    if isinstance(d, list):
        return [convert_dict_to_camel_case(i) if isinstance(i, (dict, list)) else i for i in d]
    return {to_camel_case(k): convert_dict_to_camel_case(v) if isinstance(v, (dict, list)) else v for k, v in d.items()}


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc)  + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = None):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=refresh_token_expire_days))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def decode_token(token: str) -> LoginInfo:

    try:

        if not token:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN, 
                detail = msg.get_message(msg.ME0003_SESSION_TIME_OUT),
            )

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        login_info = LoginInfo(
            user_id = int(payload.get("user_id")),
            group_id = int(payload.get("group_id")),
            owner_user_id = int(payload.get("owner_user_id")),
        )

        if not login_info.user_id:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED, 
                detail = msg.get_message(msg.ME0003_SESSION_TIME_OUT),
            )

        return login_info

    except JWTError as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = msg.get_message(msg.ME0003_SESSION_TIME_OUT)
        )

def generate_temporary_password(length=8):
    # 英字、大文字、小文字、数字、安全な記号を限定して追加
    safe_symbols = "!@#$%^&*-_=+"
    all_characters = string.ascii_letters + string.digits + safe_symbols
    return ''.join(secrets.choice(all_characters) for _ in range(length))

def generate_activation_token():
    return secrets.token_urlsafe(32)

def get_token_data(user_id: int, group_id: int, owner_user_id: int) -> TokenData:

    # トークンを生成
    login_info_dict = {"user_id": str(user_id), "group_id": str(group_id), "owner_user_id": str(owner_user_id)}
    access_token = create_access_token(login_info_dict)
    refresh_token = create_refresh_token(login_info_dict)

    return TokenData(
        access_token = access_token,
        refresh_token = refresh_token,
    )