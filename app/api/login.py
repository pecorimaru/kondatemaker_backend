from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from typing import Optional

from app.db.session import get_db
from app.utils.api_utils import CamelModel
from app.crud import UserCrud
from app.services import LoginService

from app.utils import message_utils



router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = "160003454125-03dkjca5khvs730fqfkmiguatdm8it58.apps.googleusercontent.com"

class LoginRequest(CamelModel):
    email: str
    password: Optional[str]=None

class GoogleLoginRequest(CamelModel):
    token: str

class LoginResponse(CamelModel):
    status_code: int
    message: str
    user_id: Optional[int]=None
    user_nm: Optional[str]=None


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):

    login_service = LoginService(None, db)
    user = login_service.login(request.email, request.password)

    if user:
        return LoginResponse(
            status_code = status.HTTP_200_OK,
            message = message_utils.get_message(message_utils.MI0001_LOGIN_SUCCESSFUL),
            user_id = user.user_id,
            user_nm = user.user_nm,
        )

    # user = user_crud.get_user(request.email, db)

    # if user:
    #     if user.password == request.password:
    #         return LoginResponse(
    #             status_code = status.HTTP_200_OK,
    #             message = message_utils.get_message(message_utils.MI0001_LOGIN_SUCCESSFUL),
    #             user_id = user.user_id,
    #             user_nm = user.user_nm,
    #         )

    return LoginResponse(
        status_code = status.HTTP_401_UNAUTHORIZED,
        message = message_utils.get_message("ME0001")
    )



@router.post("/googleLogin", response_model=LoginResponse)
async def google_login(request: LoginRequest, db: Session = Depends(get_db)):

    # Google のトークンを検証
    try:
        user_crud = UserCrud(None, db)
        user = user_crud.get_user(request.email)

        return LoginResponse(
            status_code = status.HTTP_200_OK,
            message = "Login Successful",
            user_id = user.user_id,
            user_nm = user.user_nm
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    


