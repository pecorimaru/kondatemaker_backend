from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import Optional, Dict


from src.utils.apiutils import CamelModel

from src.crud import ingred as ingred_crud
from src.crud import recipelist as recipelist_crud
from src.crud import common as common_crud
from src.db.session import get_db
from src.models.models import Recipe
from src.models.models import AppConst

router = APIRouter()

class RecipeIngredDisp(CamelModel):
    recipe_id: int
    recipe_ingred_id: int
    ingred_nm: str
    qty: float
    unit_nm: str


class RecipeDisp(CamelModel):
    recipe_id: int
    recipe_nm: Optional[str]=None
    recipe_nm_kana: Optional[str]
    recipe_type: Dict[str, str]
    recipe_url: Optional[str]=None
    visibility_flg: str


class SubmitAddRecipeRequest(CamelModel):
    recipe_nm: str
    recipe_nm_kana: Optional[str]=None
    recipe_type: Dict[str, str]
    recipe_url: Optional[str]=None
    user_id: int

class SubmitAddRecipeResponse(CamelModel):
    status_code: int
    message: str
    new_recipe: RecipeDisp

class SubmitEditRecipeRequest(CamelModel):
    recipe_id: int
    recipe_nm: Optional[str]=None
    recipe_nm_kana: str
    recipe_type: Dict[str, str]
    recipe_url: Optional[str]=None
    user_id: int

class SubmitEditRecipeResponse(CamelModel):
    status_code: int
    message: str
    new_recipe: RecipeDisp

class SubmitDeleteRecipeResponse(CamelModel):
    status_code: int
    message: str

class SubmitAddRecipeIngredRequest(CamelModel):
    recipe_id: int
    ingred_nm: str
    qty: float
    unit_nm: str
    user_id: int

class SubmitAddRecipeIngredResponse(CamelModel):
    status_code: int
    message: str
    new_recipe_ingred: RecipeIngredDisp



class SubmitUpdateRecipeIngredRequest(CamelModel):
    recipe_ingred_id: int
    ingred_nm: str
    qty: float
    unit_nm: str
    user_id: int

class SubmitUpdateRecipeIngredResponse(CamelModel):
    status_code: int
    message: str
    new_recipe_ingred: RecipeIngredDisp

class SubmitDeleteRecipeIngredRequest(CamelModel):
    recipe_ingred_id: int

class SubmitDeleteRecipeIngredResponse(CamelModel):
    status_code: int
    message: str


@router.get("/recipeList/{query_params}")
def fetch_recipe_list(user_id: int, db: Session = Depends(get_db)):
    
    recipe_list = recipelist_crud.get_recipe_list(user_id, db)

    recipe_disp_list = []
    for recipe in recipe_list:

        app_const = common_crud.get_app_const_from_val("C0001", recipe.recipe_type, db)
        recipe_type_nm = app_const.val_content if app_const else ""
    

        recipe_disp_list.append(
            RecipeDisp(
                recipe_id = recipe.recipe_id,
                recipe_nm = recipe.recipe_nm,
                recipe_nm_kana = recipe.recipe_nm_k,
                recipe_type = {"cd": recipe.recipe_type, "nm": recipe_type_nm},
                recipe_url = recipe.recipe_url,
                visibility_flg = recipe.visibility_flg,
            )
        )

    print(recipe_disp_list)

    return recipe_disp_list

@router.get("/recipeIngredList/{query_params}")
def fetch_recipe_ingred_list(recipe_id: int, db: Session = Depends(get_db)):


    recipe_ingred_list = recipelist_crud.get_recipe_ingred_list(recipe_id, db)

    recipe_ingred_disp_list = []
    for recipe_ingred in recipe_ingred_list:
        recipe_ingred_disp_list.append(
            RecipeIngredDisp(
                recipe_id = recipe_ingred.recipe_id,
                recipe_ingred_id = recipe_ingred.recipe_ingred_id,
                ingred_nm = recipe_ingred.ingred_nm,
                qty = recipe_ingred.qty,
                unit_nm = recipe_ingred.unit_nm
            )
        )

    print(recipe_ingred_disp_list)

    return recipe_ingred_disp_list

@router.post("/submitAddRecipe", response_model=SubmitAddRecipeResponse)
async def submit_add_recipe(request: SubmitAddRecipeRequest, db: Session = Depends(get_db)):


    new_recipe = recipelist_crud.create_recipe(request.recipe_nm, request.recipe_nm_kana, request.recipe_type, request.recipe_url, request.user_id, db)

    return SubmitAddRecipeResponse(
        status_code = 200,
        message = "Success",
        new_recipe = RecipeDisp(
            recipe_id = new_recipe.recipe_id,
            recipe_nm = new_recipe.recipe_nm,
            recipe_nm_kana = new_recipe.recipe_nm_k,
            recipe_type = {"cd": new_recipe.recipe_type, "nm": request.recipe_type["nm"]},
            recipe_url = new_recipe.recipe_url,
            visibility_flg = new_recipe.visibility_flg,
        )
    )


@router.put("/submitEditRecipe", response_model=SubmitEditRecipeResponse)
async def submit_add_recipe(request: SubmitEditRecipeRequest, db: Session = Depends(get_db)):

    new_recipe = recipelist_crud.update_recipe(request.recipe_id, request.recipe_nm, request.recipe_nm_kana, request.recipe_type, request.recipe_url, request.user_id, db)

    return SubmitEditRecipeResponse(
        status_code = 200,
        message = "Success",
        new_recipe = RecipeDisp(
            recipe_id = new_recipe.recipe_id,
            recipe_nm = new_recipe.recipe_nm,
            recipe_nm_kana = new_recipe.recipe_nm_k,
            recipe_type = {"cd": new_recipe.recipe_type, "nm": request.recipe_type["nm"]},
            recipe_url = new_recipe.recipe_url,
            visibility_flg = new_recipe.visibility_flg,
        )
    )


@router.delete("/submitDeleteRecipe/{query_params}", response_model=SubmitDeleteRecipeResponse)
async def submit_delete_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):

    print(f"recipe_id: {recipe_id}")
    result = recipelist_crud.delete_recipe(recipe_id, user_id, db)
    
    if result:
        return SubmitDeleteRecipeResponse(
        status_code = 200,
        message = "削除成功"
    )

    raise HTTPException(
        status_code = 500,
        detail = {"message": "削除失敗"}
    )



@router.post("/submitAddRecipeIngred", response_model=SubmitAddRecipeIngredResponse)
async def submit_add_recipe_ingred(request: SubmitAddRecipeIngredRequest, db: Session = Depends(get_db)):

    new_recipe_ingred = recipelist_crud.create_recipe_ingred(request.recipe_id, request.ingred_nm, request.qty, request.unit_nm, request.user_id, db)
    
    ingred = ingred_crud.get_ingred(new_recipe_ingred.ingred_id, request.user_id, db)

    unit_nm = common_crud.get_val_content("C0002", new_recipe_ingred.unit_cd, db)

    return SubmitAddRecipeIngredResponse(
        status_code = 200,
        message = "Success",
        new_recipe_ingred = RecipeIngredDisp(
            recipe_id = new_recipe_ingred.recipe_id,
            recipe_ingred_id = new_recipe_ingred.recipe_ingred_id,
            ingred_nm = ingred.ingred_nm,
            qty = new_recipe_ingred.qty,
            unit_nm = unit_nm
        )
    )


@router.put("/submitEditRecipeIngred", response_model=SubmitUpdateRecipeIngredResponse)
async def submit_update_recipe_ingred(request: SubmitUpdateRecipeIngredRequest, db: Session = Depends(get_db)):


    edit_recipe_ingred = recipelist_crud.update_recipe_ingred(request.recipe_ingred_id, request.ingred_nm, request.qty, request.unit_nm, request.user_id, db)
    
    print(edit_recipe_ingred.recipe_ingred_id)


    return SubmitAddRecipeIngredResponse(
        status_code = 200,
        message = "Success",
        new_recipe_ingred = RecipeIngredDisp(
            recipe_id = edit_recipe_ingred.recipe_id,
            recipe_ingred_id = edit_recipe_ingred.recipe_ingred_id,
            ingred_nm = request.ingred_nm,
            qty = edit_recipe_ingred.qty,
            unit_nm = request.unit_nm,
        )
    )


@router.delete("/submitDeleteRecipeIngred/{query_params}", response_model=SubmitDeleteRecipeIngredResponse)
async def submit_delete_recipe_ingred(recipe_ingred_id: int, db: Session = Depends(get_db)):

    print(f"recipe_ingred_id: {recipe_ingred_id}")
    result = recipelist_crud.delete_recipe_ingred(recipe_ingred_id, db)
    
    if result:
        return SubmitDeleteRecipeIngredResponse(
        status_code = 200,
        message = "削除成功"
    )

    raise HTTPException(
        status_code = 500,
        detail = {"message": "削除失敗"}
    )
