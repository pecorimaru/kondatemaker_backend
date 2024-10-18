from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.utils.apiutils import CamelModel
from src.crud import common as common_crud
from src.crud import inputingred as inputingred_crud
from src.db.session import get_db

import src.utils.dbutils as dbutils

router = APIRouter()


class RecipeType(CamelModel):
    cd: str
    nm: str

class FetchRecipeTypeResponse(CamelModel):
    status_code: int
    message: str
    recipe_type_list: list[RecipeType]



@router.get("/recipeTypeList")
def fetch_unit_list(db: Session = Depends(get_db)):
    
    app_consts = common_crud.get_app_consts("C0001", db)

    recipe_type_list = []
    for app_const in app_consts:
        recipe_type_list.append(RecipeType(
            cd=app_const.val,
            nm=app_const.val_content
        ))

    return recipe_type_list

