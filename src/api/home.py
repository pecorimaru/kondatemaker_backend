from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.utils.apiutils import CamelModel
from src.crud import home as home_crud
from src.db.session import get_db

router = APIRouter()

class RefreshToweekPlanResponse(CamelModel):
    status_code: int
    message: str

class RefreshToweekPlanRequest(CamelModel):
    selected_plan: str
    user_id: int

@router.get("/menuPlanNm/{query_params}")
def fetch_menu_plan_nm(user_id: int, db: Session = Depends(get_db)):

    menu_plan = home_crud.get_toweek_menu_plan(user_id, db)
    if menu_plan:
        menu_plan_nm =  menu_plan.menu_plan_nm
    else:
        menu_plan_nm = "選択してください"

    print(menu_plan_nm)
    return menu_plan_nm


@router.get("/menuPlanList/{query_params}")
def fetch_menu_plan_list(user_id: int, db: Session = Depends(get_db)):

    menu_plan_list = home_crud.get_menu_plan_list(user_id, db)
    print(menu_plan_list)
    return menu_plan_list


@router.get("/toweekRecipes/{query_params}")
def fetch_toweek_recipes(selected_plan: str, user_id: int, db: Session = Depends(get_db)):
    
    toweek_recipes = home_crud.get_toweek_recipes(selected_plan, user_id, db)
    print(toweek_recipes)
    return toweek_recipes




@router.put("/refreshToweekPlan", response_model=RefreshToweekPlanResponse)
async def refresh_toweek_plan(request: RefreshToweekPlanRequest, db: Session = Depends(get_db)):

    home_crud.delete_toweek_recipes(request.user_id, db)
    home_crud.delete_buy_ingreds(request.user_id, db)

    home_crud.update_toweek_plan(request.selected_plan, request.user_id, db)
    home_crud.create_toweek_recipes(request.selected_plan, request.user_id, db)
    home_crud.create_buy_ingreds(request.user_id, db)

    return RefreshToweekPlanResponse(
        status_code = 200,
        message = "Refresh Successful"
    )

