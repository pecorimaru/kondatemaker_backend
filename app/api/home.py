from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional, Dict

from app.db.session import get_db
from app.utils.api_utils import CamelModel
from app.models.display import MenuPlanDisp, ToweekMenuPlanDetDisp
from app.services import HomeService


router = APIRouter()


class SubmitRecreateToweekPlanRequest(CamelModel):
    selected_plan_id: int
    user_id: int

class SubmitRecreateToweekPlanResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_toweek_menu_plan_det_list_dict: Dict[str, list]

class SubmitAddToweekMenuPlanDetRequest(CamelModel):
    recipe_nm: str
    weekday_cd: str
    user_id: int

class SubmitAddToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_toweek_menu_plan_det: ToweekMenuPlanDetDisp

class SubmitEditToweekMenuPlanDetRequest(CamelModel):
    toweek_menu_plan_det_id: int
    recipe_nm: str
    user_id: int

class SubmitEditToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    edit_toweek_menu_plan_det: ToweekMenuPlanDetDisp

class SubmitDeleteToweekMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/slectedPlan/{query_params}")
def fetch_selected_plan(user_id: int, db: Session = Depends(get_db)) -> MenuPlanDisp:

    # 前回選択した献立プランを取得
    home_service = HomeService(user_id, db)
    selected_plan = home_service.fetch_selected_plan()
    return selected_plan


@router.get("/toweekMenuPlanDetListDict/{query_params}")
def fetch_toweek_menu_plan_det_list(user_id: int, db: Session = Depends(get_db)) -> dict[str, list]:

    # 前回セットした献立明細を取得
    home_service = HomeService(user_id, db)
    toweek_menu_plan_det_list_dict = home_service.fetch_toweek_menu_plan_det()
    return toweek_menu_plan_det_list_dict


@router.put("/submitRecreateToweekMenuPlan", response_model=SubmitRecreateToweekPlanResponse)
def submit_recreate_toweek_plan(request: SubmitRecreateToweekPlanRequest, db: Session = Depends(get_db)):

    home_service = HomeService(request.user_id, db)
    new_toweek_menu_plan_det_list_dict = home_service.recreate_toweek_plan(request.selected_plan_id)
    return SubmitRecreateToweekPlanResponse(
        status_code = status.HTTP_200_OK,
        new_toweek_menu_plan_det_list_dict = new_toweek_menu_plan_det_list_dict,
    )


@router.post("/submitAddToweekMenuPlanDet", response_model=SubmitAddToweekMenuPlanDetResponse)
def submit_add_toweek_menu_plan_det(request: SubmitAddToweekMenuPlanDetRequest, db: Session = Depends(get_db)):

    home_service = HomeService(request.user_id, db)
    new_toweek_menu_plan_det = home_service.add_toweek_menu_plan_det(request.recipe_nm, request.weekday_cd)

    return SubmitAddToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
        new_toweek_menu_plan_det = new_toweek_menu_plan_det,
    )


@router.put("/submitEditToweekMenuPlanDet", response_model=SubmitEditToweekMenuPlanDetResponse)
def submit_edit_toweek_menu_plan_det(request: SubmitEditToweekMenuPlanDetRequest, db: Session = Depends(get_db)):

    home_service = HomeService(request.user_id, db)
    edit_toweek_menu_plan_det = home_service.edit_toweek_menu_plan_det(request.toweek_menu_plan_det_id, request.recipe_nm)

    return SubmitEditToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
        edit_toweek_menu_plan_det = edit_toweek_menu_plan_det,
    )


@router.delete("/submitDeleteToweekMenuPlanDet/{query_params}")
def submit_delete_toweek_menu_plan_det(toweek_menu_plan_det_id: int, user_id: int, db: Session = Depends(get_db)):

    home_service = HomeService(user_id, db)
    home_service.delete_toweek_menu_plan_det(toweek_menu_plan_det_id)

    return SubmitDeleteToweekMenuPlanDetResponse(
        status_code = status.HTTP_200_OK,
    )
