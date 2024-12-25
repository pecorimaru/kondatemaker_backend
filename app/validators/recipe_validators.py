from fastapi import HTTPException, status

from app.models import Recipe, MenuPlanDet
from app.crud import RecipeCrud
from app.utils import constants as const, message_utils as msg


def exist_recipe(recipe: Recipe, recipe_nm: str):
    if not recipe:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "レシピ", recipe_nm),
        )


def recipe_not_duplicate(recipe: Recipe, recipe_nm: str):
    if recipe:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, recipe_nm),
        )


def recipe_not_referenced(menu_plan_det_list: list[MenuPlanDet], recipe_crud: RecipeCrud, recipe_id:int):
    # 削除対象のレシピが献立明細に参照されていた場合
    if menu_plan_det_list:
        menu_plan_example = menu_plan_det_list[0].rel_t_menu_plan.menu_plan_nm
        menu_plan_other = "など" if len(menu_plan_det_list) > 1 else ""
        recipe = recipe_crud.get_recipe(recipe_id)
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(
                msg.ME0012_NOT_DELETABLE_FOREIGN_KEY, 
                recipe.recipe_nm, 
                "献立プラン", 
                menu_plan_example, 
                menu_plan_other
            ),
        )


def ingred_not_duplicate(recipe_ingred: int, ingred_nm: str):
    if recipe_ingred:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0013_INGRED_ALREADY_EXISTS, recipe_ingred.rel_t_recipe.recipe_nm, ingred_nm),
        )