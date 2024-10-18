from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.crud import login as login_crud
from src.db.session import get_db
from src.utils.apiutils import convert_dict_to_camel_case

router = APIRouter()

GOOGLE_CLIENT_ID = "160003454125-03dkjca5khvs730fqfkmiguatdm8it58.apps.googleusercontent.com"

class LoginRequest(BaseModel):
    email: str
    password: Optional[str]=None

class GoogleLoginRequest(BaseModel):
    token: str

class LoginResponse(BaseModel):
    status_code: int
    message: str
    id: Optional[int]=None
    name: Optional[str]=None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):

    try:

        user = login_crud.get_user(request.email, db)
        if user:
            if user.password == request.password:
                return LoginResponse(
                    status_code = status.HTTP_200_OK,
                    message = "Login Successful",
                    id = user.user_id,
                    name = user.user_nm
                )

        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content = convert_dict_to_camel_case({
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "message": "ログインに失敗しました。",
                "id": None,
                "name": None
            })
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/googleLogin", response_model=LoginResponse)
async def google_login(request: LoginRequest, db: Session = Depends(get_db)):

    # Google のトークンを検証
    try:
        user = login_crud.get_user(request.email, db)

        return LoginResponse(
            status_code = status.HTTP_200_OK,
            message = "Login Successful",
            id = user.user_id,
            name = user.user_nm
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    


