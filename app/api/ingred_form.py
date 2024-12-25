from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.session import get_db, oauth2_scheme
from app.services import IngredFormService
from app.models.display import DefaultSets
from app.utils.api_utils import decode_token


router = APIRouter()


@router.get("/defaultSetsByIngred/{query_params}")
def fetch_default_sets_by_ingred(ingred_nm: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    if not ingred_nm:
        return None

    ingred_form_service = IngredFormService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    default_sets = ingred_form_service.fetch_default_sets_by_ingred(ingred_nm)
    return default_sets


@router.get("/unitDictByIngred/{query_params}")
def fetch_unit_dict_by_ingred(ingred_nm: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    login_info = decode_token(token)

    ingred_form_service = IngredFormService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    unit_dict_by_ingred = ingred_form_service.fetch_unit_dict_by_ingred(ingred_nm)
    return unit_dict_by_ingred


@router.get("/ingredNmSuggestions/{query_params}")
def fetch_ingred_nm_suggestions(input_value: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> list[str]:
    login_info = decode_token(token)

    if not (input_value):
        return []

    ingred_form_service = IngredFormService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    ingred_nm_suggestions = ingred_form_service.fetch_ingred_nm_suggestions(input_value)
    return ingred_nm_suggestions

