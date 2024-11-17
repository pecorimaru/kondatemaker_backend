from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Optional

from app.db.session import get_db
from app.utils.api_utils import CamelModel
from app.models.display import MenuPlanDisp, MenuPlanDetDisp

from app.services import MenuPlanService


router = APIRouter()


class SubmitAddMenuPlanRequest(CamelModel):
    menu_plan_nm: str
    menu_plan_nm_k: str
    user_id: int

class SubmitAddMenuPlanResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_menu_plan: MenuPlanDisp

class SubmitEditMenuPlanRequest(CamelModel):
    menu_plan_id: int
    menu_plan_nm: str
    menu_plan_nm_k: str
    user_id: int

class SubmitEditMenuPlanResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_menu_plan: MenuPlanDisp

class SubmitDeleteMenuPlanResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitAddMenuPlanDetRequest(CamelModel):
    menu_plan_id: int
    weekday_cd: str
    recipe_nm: str 
    user_id: int

class SubmitAddMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_menu_plan_det: MenuPlanDetDisp

class SubmitEditMenuPlanDetRequest(CamelModel):
    menu_plan_det_id: int
    weekday_cd: str
    recipe_nm: str 
    user_id: int

class SubmitEditMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_menu_plan_det: MenuPlanDetDisp

class SubmitDeleteMenuPlanDetResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/menuPlanList/{query_params}")
def fetch_menu_plan_list(user_id: int, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(user_id, db)
    menu_plan_list = menu_plan_service.fetch_menu_plan_list()
    return menu_plan_list


@router.get("/menuPlanDetList/{query_params}")
def fetch_menu_plan_det_list(menu_plan_id: int, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(None, db)
    menu_plan_det_list = menu_plan_service.fetch_menu_plan_det_list(menu_plan_id)
    return menu_plan_det_list


@router.post("/submitAddMenuPlan", response_model=SubmitAddMenuPlanResponse)
async def submit_add_menu_plan(request: SubmitAddMenuPlanRequest, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(request.user_id, db)
    new_menu_plan = menu_plan_service.add_menu_plan(request.menu_plan_nm, request.menu_plan_nm_k)

    return SubmitAddMenuPlanResponse(
        status_code = 200,
        new_menu_plan = new_menu_plan
    )


@router.put("/submitEditMenuPlan", response_model=SubmitEditMenuPlanResponse)
async def submit_edit_menu_plan(request: SubmitEditMenuPlanRequest, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(request.user_id, db)
    new_menu_plan = menu_plan_service.edit_menu_plan(request.menu_plan_id, request.menu_plan_nm, request.menu_plan_nm_k)

    return SubmitEditMenuPlanResponse(
        status_code = 200,
        new_menu_plan = new_menu_plan
    )


@router.delete("/submitDeleteMenuPlan/{query_params}", response_model=SubmitDeleteMenuPlanResponse)
async def submit_delete_menu_plan(menu_plan_id: int, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(None, db)
    menu_plan_service.delete_menu_plan(menu_plan_id)

    return SubmitDeleteMenuPlanResponse(
        status_code = 200,
    )


@router.post("/submitAddMenuPlanDet", response_model=SubmitAddMenuPlanDetResponse)
async def submit_add_menu_plan_det(request: SubmitAddMenuPlanDetRequest, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(request.user_id, db)
    new_menu_plan_det = menu_plan_service.add_menu_plan_det(request.menu_plan_id, request.weekday_cd, request.recipe_nm)

    return SubmitAddMenuPlanDetResponse(
        status_code = 200,
        new_menu_plan_det = new_menu_plan_det
    )

@router.put("/submitEditMenuPlanDet", response_model=SubmitEditMenuPlanDetResponse)
async def submit_edit_menu_plan(request: SubmitEditMenuPlanDetRequest, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(request.user_id, db)
    new_menu_plan_det = menu_plan_service.edit_menu_plan_det(request.menu_plan_det_id, request.weekday_cd, request.recipe_nm)

    return SubmitEditMenuPlanDetResponse(
        status_code = 200,
        new_menu_plan_det = new_menu_plan_det
    )

@router.delete("/submitDeleteMenuPlanDet/{query_params}", response_model=SubmitDeleteMenuPlanDetResponse)
async def submit_delete_menu_plan_det(menu_plan_det_id: int, db: Session = Depends(get_db)):

    menu_plan_service = MenuPlanService(None, db)
    menu_plan_service.delete_menu_plan_det(menu_plan_det_id)

    return SubmitDeleteMenuPlanResponse(
        status_code = 200,
    )

