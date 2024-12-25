from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import CamelModel
from app.models.display import IngredDisp, IngredUnitConvDisp
from app.services import IngredService
from app.utils.api_utils import decode_token
from app.utils import message_utils as msg

router = APIRouter()


class SubmitAddIngredRequest(CamelModel):
    ingred_nm: str
    ingred_nm_k: Optional[str]=None
    parent_ingred_nm: str
    buy_unit_cd: str
    sales_area_type: Optional[str]=None

class SubmitAddIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred: IngredDisp

class SubmitEditIngredRequest(CamelModel):
    ingred_id: int
    ingred_nm: str
    ingred_nm_k: Optional[str]=None
    parent_ingred_nm: str
    buy_unit_cd: str
    sales_area_type: Optional[str]=None

class SubmitEditIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    edit_ingred: IngredDisp

class SubmitDeleteIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitAddIngredUnitConvRequest(CamelModel):
    ingred_id: int
    conv_unit_cd: str
    conv_rate: float

class SubmitAddIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred_unit_conv: IngredUnitConvDisp

class SubmitUpdateIngredUnitConvRequest(CamelModel):
    ingred_unit_conv_id: int
    ingred_id: int
    conv_unit_cd: str
    conv_rate: float

class SubmitUpdateIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred_unit_conv: IngredUnitConvDisp

class SubmitDeleteIngredUnitConvRequest(CamelModel):
    ingred_unit_conv_id: int

class SubmitDeleteIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/ingredList")
def fetch_ingred_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    ingred_list = ingred_service.fetch_ingred_list()
    return ingred_list


@router.post("/submitAddIngred", response_model=SubmitAddIngredResponse)
def submit_add_ingred(request: SubmitAddIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_ingred = ingred_service.add_ingred(request.ingred_nm, request.ingred_nm_k, request.parent_ingred_nm, request.buy_unit_cd, request.sales_area_type)
    return SubmitAddIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        new_ingred = new_ingred,
    )


@router.put("/submitEditIngred", response_model=SubmitEditIngredResponse)
def submit_edit_ingred(request: SubmitEditIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    edit_ingred = ingred_service.edit_ingred(request.ingred_id, request.ingred_nm, request.ingred_nm_k, request.parent_ingred_nm, request.buy_unit_cd, request.sales_area_type)
    return SubmitEditIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        edit_ingred = edit_ingred
    )


@router.delete("/submitDeleteIngred/{query_params}", response_model=SubmitDeleteIngredResponse)
def submit_delete_ingred(ingred_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    ingred_service.delete_ingred(ingred_id)
    return SubmitDeleteIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )


@router.get("/ingredUnitConvList/{query_params}")
def fetch_ingred_unit_conv_list(ingred_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    ingred_unit_conv_list = ingred_service.fetch_ingred_unit_conv_list(ingred_id)
    return ingred_unit_conv_list


@router.post("/submitAddIngredUnitConv", response_model=SubmitAddIngredUnitConvResponse)
def submit_add_ingred_unit_conv(request: SubmitAddIngredUnitConvRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_ingred_unit_conv = ingred_service.add_ingred_unit_conv(request.ingred_id, request.conv_unit_cd, request.conv_rate)
    return SubmitAddIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        new_ingred_unit_conv = new_ingred_unit_conv
    )


@router.put("/submitEditIngredUnitConv", response_model=SubmitUpdateIngredUnitConvResponse)
def submit_edit_ingred_unit_conv(request: SubmitUpdateIngredUnitConvRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_ingred_unit_conv = ingred_service.edit_ingred_unit_conv(request.ingred_unit_conv_id, request.ingred_id, request.conv_unit_cd, request.conv_rate)
    return SubmitAddIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_ingred_unit_conv = new_ingred_unit_conv,
    )


@router.delete("/submitDeleteIngredUnitConv/{query_params}", response_model=SubmitDeleteIngredUnitConvResponse)
async def submit_delete_ingred_unit_conv(ingred_unit_conv_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    ingred_service = IngredService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    ingred_service.delete_ingred_unit_conv(ingred_unit_conv_id)
    return SubmitDeleteIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )
