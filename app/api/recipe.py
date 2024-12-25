from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional

from app.core.session import get_db, oauth2_scheme
from app.utils.api_utils import CamelModel
from app.models.display import RecipeDisp, RecipeIngredDisp
from app.services import RecipeService
from app.utils.api_utils import decode_token
from app.utils import message_utils as msg


router = APIRouter()


class SubmitAddRecipeRequest(CamelModel):
    recipe_nm: str
    recipe_nm_k: Optional[str]=None
    recipe_type: str
    recipe_url: Optional[str]=None

class SubmitAddRecipeResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_recipe: RecipeDisp

class SubmitEditRecipeRequest(CamelModel):
    recipe_id: int
    recipe_nm: str
    recipe_nm_k: Optional[str]=None
    recipe_type: str
    recipe_url: Optional[str]=None

class SubmitEditRecipeResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_recipe: RecipeDisp

class SubmitDeleteRecipeResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitAddRecipeIngredRequest(CamelModel):
    recipe_id: int
    ingred_nm: str
    qty: float
    unit_cd: str

class SubmitAddRecipeIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_recipe_ingred: RecipeIngredDisp

class SubmitUpdateRecipeIngredRequest(CamelModel):
    recipe_ingred_id: int
    ingred_nm: str
    qty: float
    unit_cd: str

class SubmitUpdateRecipeIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_recipe_ingred: RecipeIngredDisp

class SubmitDeleteRecipeIngredRequest(CamelModel):
    recipe_ingred_id: int

class SubmitDeleteRecipeIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/recipeList")
def fetch_recipe_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)
    
    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    recipe_list = recipe_service.fetch_recipe_list()
    return recipe_list


@router.get("/recipeIngredList/{query_params}")
def fetch_recipe_ingred_list(recipe_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    recipe_ingred_list = recipe_service.fetch_recipe_ingred_list(recipe_id)
    return recipe_ingred_list


@router.post("/submitAddRecipe", response_model=SubmitAddRecipeResponse)
async def submit_add_recipe(request: SubmitAddRecipeRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_recipe = recipe_service.add_recipe(request.recipe_nm, request.recipe_nm_k, request.recipe_type, request.recipe_url)
    return SubmitAddRecipeResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        new_recipe = new_recipe,
    )


@router.put("/submitEditRecipe", response_model=SubmitEditRecipeResponse)
async def submit_edit_recipe(request: SubmitEditRecipeRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_recipe = recipe_service.edit_recipe(request.recipe_id, request.recipe_nm, request.recipe_nm_k, request.recipe_type, request.recipe_url)
    return SubmitEditRecipeResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_recipe = new_recipe
    )


@router.delete("/submitDeleteRecipe/{query_params}", response_model=SubmitDeleteRecipeResponse)
async def submit_delete_recipe(recipe_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    recipe_service.delete_recipe(recipe_id)
    return SubmitDeleteRecipeResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )


@router.post("/submitAddRecipeIngred", response_model=SubmitAddRecipeIngredResponse)
async def submit_add_recipe_ingred(request: SubmitAddRecipeIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_recipe_ingred = recipe_service.add_recipe_ingred(request.recipe_id, request.ingred_nm, request.qty, request.unit_cd)
    return SubmitAddRecipeIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0002_CREATE_SUCCESSFUL),
        new_recipe_ingred = new_recipe_ingred
    )


@router.put("/submitEditRecipeIngred", response_model=SubmitUpdateRecipeIngredResponse)
async def submit_edit_recipe_ingred(request: SubmitUpdateRecipeIngredRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    new_recipe_ingred = recipe_service.edit_recipe_ingred(request.recipe_ingred_id, request.ingred_nm, request.qty, request.unit_cd)
    return SubmitAddRecipeIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0003_EDIT_SUCCESSFUL),
        new_recipe_ingred = new_recipe_ingred,
    )


@router.delete("/submitDeleteRecipeIngred/{query_params}", response_model=SubmitDeleteRecipeIngredResponse)
async def submit_delete_recipe_ingred(recipe_ingred_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    login_info = decode_token(token)

    recipe_service = RecipeService(login_info.user_id, login_info.group_id, login_info.owner_user_id, db)
    recipe_service.delete_recipe_ingred(recipe_ingred_id)
    return SubmitDeleteRecipeIngredResponse(
        status_code = status.HTTP_200_OK,
        message = msg.get_message(msg.MI0008_DELETE_SUCCESSFUL),
    )
