from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.session import get_db

from app.services import AppConstService
from app.utils import constants as const


router = APIRouter()


@router.get("/recipeTypeDict")
async def fetch_recipe_type_dict(db: Session = Depends(get_db)):

    const_service = AppConstService(db)
    recipe_type_dict = const_service.fetch_app_const_dict(const.APP_CONST_C0001_RECIPE_TYPE)
    return recipe_type_dict


@router.get("/unitDict")
def fetch_unit_dict(db: Session = Depends(get_db)):

    const_service = AppConstService(db)
    unit_dict = const_service.fetch_app_const_dict(const.APP_CONST_C0002_UNIT_TYPE)
    return unit_dict


@router.get("/salesAreaDict")
def fetch_sales_area_dict(db: Session = Depends(get_db)):

    const_service = AppConstService(db)
    sales_area_dict = const_service.fetch_app_const_dict(const.APP_CONST_C0004_SALES_AREA_TYPE)
    return sales_area_dict


@router.get("/weekdayDict")
def fetch_weekday_dict(db: Session = Depends(get_db)):

    const_service = AppConstService(db)
    weekday_dict = const_service.fetch_app_const_dict(const.APP_CONST_C0005_WEEKDAY_TYPE)
    return weekday_dict
