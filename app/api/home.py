from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional, Dict

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import CamelModel, decode_token
from app.models.display import MenuPlanDisp, ToweekMenuPlanDetDisp
from app.services import HomeService
from app.utils import message_utils as msg


router = APIRouter()


class SubmitRecreateToweekPlanRequest(CamelModel):
    selected_plan_id: int

class SubmitRecreateToweekPlanResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_toweek_menu_plan_det_list_dict: Dict[str, list]

class SubmitAddToweekMenuPlanDetRequest(CamelModel):
    recipe_nm: str
    weekday_cd: str

class SubmitAddToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    toweek_menu_plan_det_list_dict: Dict[str, list]

class SubmitEditToweekMenuPlanDetRequest(CamelModel):
    toweek_menu_plan_det_id: int
    recipe_nm: str

class SubmitEditToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    toweek_menu_plan_det_list_dict: Dict[str, list]

class SubmitDeleteToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/slectedPlan")
def fetch_selected_plan(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    # 前回選択した献立プランを取得
    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    selected_plan = home_service.fetch_selected_plan()
    return selected_plan


@router.get("/toweekMenuPlanDetListDict")
def fetch_toweek_menu_plan_det_list_dict(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> dict[str, list]:
    login_info = decode_token(token)

    # 前回セットした献立明細を取得
    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    toweek_menu_plan_det_list_dict = home_service.fetch_toweek_menu_plan_det()
    return toweek_menu_plan_det_list_dict


@router.put("/submitRecreateToweekMenuPlan", response_model=SubmitRecreateToweekPlanResponse)
def submit_recreate_toweek_plan(request: SubmitRecreateToweekPlanRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_toweek_menu_plan_det_list_dict = home_service.recreate_toweek_plan(request.selected_plan_id)
    return SubmitRecreateToweekPlanResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_toweek_menu_plan_det_list_dict = new_toweek_menu_plan_det_list_dict,
    )


@router.post("/submitAddToweekMenuPlanDet", response_model=SubmitAddToweekMenuPlanDetResponse)
def submit_add_toweek_menu_plan_det(request: SubmitAddToweekMenuPlanDetRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    toweek_menu_plan_det_list_dict = home_service.add_toweek_menu_plan_det(request.recipe_nm, request.weekday_cd)

    return SubmitAddToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        toweek_menu_plan_det_list_dict = toweek_menu_plan_det_list_dict,
    )


@router.put("/submitEditToweekMenuPlanDet", response_model=SubmitEditToweekMenuPlanDetResponse)
def submit_edit_toweek_menu_plan_det(request: SubmitEditToweekMenuPlanDetRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    toweek_menu_plan_det_list_dict = home_service.edit_toweek_menu_plan_det(request.toweek_menu_plan_det_id, request.recipe_nm)

    return SubmitEditToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        toweek_menu_plan_det_list_dict = toweek_menu_plan_det_list_dict,
    )


@router.delete("/submitDeleteToweekMenuPlanDet/{query_params}")
def submit_delete_toweek_menu_plan_det(toweek_menu_plan_det_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)
    
    home_service = HomeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    home_service.delete_toweek_menu_plan_det(toweek_menu_plan_det_id)

    return SubmitDeleteToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )
