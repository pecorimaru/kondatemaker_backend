from fastapi import APIRouter, Depends, status, Request, Response, HTTPException
from sqlalchemy.orm import Session

from typing import Optional

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import CamelModel, decode_token
from app.models.display import GroupDisp, GroupMemberDisp
from app.services import SettingService
from app.utils import message_utils as msg


router = APIRouter()


class SubmitEditUserNmRequest(CamelModel):
    edit_user_nm: str

class SubmitEditUserNmResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitChangePasswordRequest(CamelModel):
    current_password: str
    new_password: str

class SubmitChangePasswordResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitDeleteUserResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitEditGroupNmRequest(CamelModel):
    edit_group_nm: str

class SubmitEditGroupNmResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    edit_group: GroupDisp

class SubmitMemberInviteRequest(CamelModel):
    to_email: str

class SubmitMemberInviteResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class JoinGroupRequest(CamelModel):
    token: str

class JoinGroupResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class ChangeGroupRequest(CamelModel):
    group_id: int

class ChangeGroupResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    access_token: Optional[str]=None

class ExitGroupResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    access_token: Optional[str]=None

class LogoutResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.post("/submitEditUserNm", response_model=SubmitEditUserNmResponse)
async def submit_edit_user_nm(request: SubmitEditUserNmRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    setting_service.edit_user_nm(request.edit_user_nm)

    return SubmitEditUserNmResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
    )


@router.post("/submitChangePassword", response_model=SubmitChangePasswordResponse)
async def submit_change_password(request: SubmitChangePasswordRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    setting_service.change_password(request.current_password, request.new_password)

    return SubmitChangePasswordResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0007_CHANGE_PASSWORD_DONE),
    )


@router.delete("/submitDeleteUser", response_model=SubmitDeleteUserResponse)
async def submit_delete_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    setting_service.delete_user()

    return SubmitDeleteUserResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )


@router.get("/loginUser/{query_params}")
def fetch_user_nm(is_logged_in: bool, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    # if not is_logged_in:
    #     return None
    
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    login_user = setting_service.fetch_login_user()
    return login_user


@router.get("/currentGroup/{query_params}")
def fetch_current_group(is_logged_in: bool, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    # if not is_logged_in:
    #     return None

    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    group_disp = setting_service.fetch_current_group()
    return group_disp


@router.get("/groupList")
def fetch_group_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> list[GroupDisp]:
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    group_disp_list = setting_service.fetch_group_list()
    return group_disp_list


@router.get("/groupMemberList")
def fetch_group_member_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> list[GroupMemberDisp]:
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    group_member_disp_list = setting_service.fetch_group_member_list()
    return group_member_disp_list


@router.post("/submitEditGroupNm", response_model=SubmitEditGroupNmResponse)
async def submit_edit_group_nm(request: SubmitEditGroupNmRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    edit_group_disp = setting_service.edit_group_nm(request.edit_group_nm)

    return SubmitEditGroupNmResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        edit_group = edit_group_disp,
    )


@router.post("/submitMemberInvite", response_model=SubmitMemberInviteResponse)
async def submit_edit_group_nm(request: SubmitMemberInviteRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    setting_service.member_invite(request.to_email)

    return SubmitMemberInviteResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0009_MEMBER_INVENT_DONE),
    )


@router.post("/joinGroup", response_model=JoinGroupResponse)
def activate_user(request: JoinGroupRequest, db: Session = Depends(get_db)):

    setting_service = SettingService(None, None, None, db)
    setting_service.join_group(request.token)

    return JoinGroupResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0006_ACTIVATE_USER_DONE),
    )


@router.post("/changeGroup", response_model=ChangeGroupResponse)
def change_group(request: ChangeGroupRequest, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    token_data = setting_service.change_group(request.group_id)

    # クッキーにリフレッシュトークンをセット
    response.set_cookie(
        key="refresh_token",
        value=token_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7日間
    )

    return ChangeGroupResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0006_ACTIVATE_USER_DONE),
        access_token = token_data.access_token,
    )


@router.post("/exitGroup", response_model=ExitGroupResponse)
def exit_group(response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    setting_service = SettingService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    token_data = setting_service.exit_group()

    # クッキーにリフレッシュトークンをセット
    response.set_cookie(
        key="refresh_token",
        value=token_data.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=7 * 24 * 60 * 60  # 7日間
    )

    return ExitGroupResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0006_ACTIVATE_USER_DONE),
        access_token = token_data.access_token,
    )


@router.post("/logout", response_model=LogoutResponse)
async def submit_edit_user_nm(request: Request, response: Response):

    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        # # クッキーにリフレッシュトークンをセット
        # response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     secure=True,
        #     samesite="Strict",
        #     max_age=0
        # )

    return LogoutResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0010_LOGOUT_DONE),
    )