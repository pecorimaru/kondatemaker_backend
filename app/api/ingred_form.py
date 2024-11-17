from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import IngredFormService


router = APIRouter()


@router.get("/defaultSetsByIngred/{query_params}")
def fetch_default_sets_by_ingred(ingred_nm: str, user_id: int, db: Session = Depends(get_db)):
    
    ingred_form_service = IngredFormService(user_id, db)
    default_sets = ingred_form_service.fetch_default_sets_by_ingred(ingred_nm)
    return default_sets


@router.get("/unitDictByIngred/{query_params}")
def fetch_unit_dict_by_ingred(ingred_nm: str, user_id: int, db: Session = Depends(get_db)):
    
    ingred_form_service = IngredFormService(user_id, db)
    unit_dict_by_ingred = ingred_form_service.fetch_unit_dict_by_ingred(ingred_nm)
    return unit_dict_by_ingred


@router.get("/ingredNmSuggestions/{query_params}")
def fetch_ingred_nm_suggestions(input_value: str, user_id: int, db: Session = Depends(get_db)) -> list[str]:
    
    if not (input_value):
        return []

    ingred_form_service = IngredFormService(user_id, db)
    ingred_nm_suggestions = ingred_form_service.fetch_ingred_nm_suggestions(input_value)
    return ingred_nm_suggestions


