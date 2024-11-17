from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Optional

from app.db.session import get_db
from app.utils.api_utils import CamelModel

from app.services import RecipeFormService


router = APIRouter()


class RecipeNmSuggestion(CamelModel):
    recipe_nm: str
    recipe_nm_k: Optional[str]=None


@router.get("/recipeNmSuggestions/{query_params}")
def fetch_recipe_nm_suggestions(input_value: str, user_id: int, db: Session = Depends(get_db)):
    
    if not (input_value):
        return []
    
    recipe_form_service = RecipeFormService(user_id, db)
    recipe_nm_suggestions = recipe_form_service.fetch_recipe_nm_suggestions(input_value) 
   
    return recipe_nm_suggestions

