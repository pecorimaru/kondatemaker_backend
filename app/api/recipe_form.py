from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import decode_token

from app.services import RecipeFormService


router = APIRouter()


@router.get("/recipeNmSuggestions/{query_params}")
def fetch_recipe_nm_suggestions(input_value: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)
    
    if not (input_value):
        return []
    
    recipe_form_service = RecipeFormService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    recipe_nm_suggestions = recipe_form_service.fetch_recipe_nm_suggestions(input_value) 
   
    return recipe_nm_suggestions

