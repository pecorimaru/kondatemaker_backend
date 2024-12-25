from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import CamelModel, decode_token
from app.models.display import BuyIngredDisp
from app.services import BuyService
from app.utils import message_utils as msg


router = APIRouter()


class SwitchCompletionStateRequest(CamelModel):
    buy_ingred_id: int
    bought_flg: str

class SwitchCompletionStateResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_buy_ingred: BuyIngredDisp

class SubmitAddBuyIngredRequest(CamelModel):
    ingred_nm: str
    qty: float
    unit_cd: str
    sales_area_type: str

class SubmitAddBuyIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_buy_ingred: BuyIngredDisp

class SubmitEditBuyIngredRequest(CamelModel):
    buy_ingred_id: int
    ingred_nm: str
    qty: float
    unit_cd: str
    sales_area_type: str

class SubmitEditBuyIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_buy_ingred: BuyIngredDisp

class SubmitDeleteBuyIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/buyIngredList")
def fetch_buy_ingred_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> list[BuyIngredDisp]:
    login_info = decode_token(token)

    buy_service = BuyService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    buy_ingred_list = buy_service.fetch_buy_ingred_list()
    return buy_ingred_list


@router.put("/submitSwitchCompletion", response_model=SwitchCompletionStateResponse)
def submit_switch_completion_state(request: SwitchCompletionStateRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    buy_service = BuyService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_buy_ingred = buy_service.switch_completion_state(request.buy_ingred_id, request.bought_flg)
    return SwitchCompletionStateResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_buy_ingred = new_buy_ingred
    )


@router.post("/submitAddBuyIngred", response_model=SubmitAddBuyIngredResponse)
def submit_add_buy_ingred(request: SubmitAddBuyIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    buy_service = BuyService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_buy_ingred = buy_service.add_buy_ingred(request.ingred_nm, request.qty, request.unit_cd, request.sales_area_type)
    return SubmitAddBuyIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        new_buy_ingred = new_buy_ingred
    )


@router.put("/submitEditBuyIngred", response_model=SubmitEditBuyIngredResponse)
def submit_edit_buy_ingred(request: SubmitEditBuyIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    buy_service = BuyService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_buy_ingred = buy_service.edit_buy_ingred(request.buy_ingred_id, request.ingred_nm, request.qty, request.unit_cd, request.sales_area_type)
    return SubmitEditBuyIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_buy_ingred = new_buy_ingred,
    )


@router.delete("/submitDeleteBuyIngred/{query_params}", response_model=SubmitDeleteBuyIngredResponse)
def submit_delete_buy_ingred(buy_ingred_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    buy_service = BuyService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    buy_service.delete_buy_ingred(buy_ingred_id)
    return SubmitDeleteBuyIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )
    
