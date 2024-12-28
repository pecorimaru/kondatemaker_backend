from fastapi import HTTPException, status

from app.models import Recipe, RecipeIngred, MenuPlanDet
from app.utils import message_utils as msg


def check_recipe_exists(recipe: Recipe, recipe_nm: str):
    if not recipe:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "レシピ", recipe_nm),
        )


def check_recipe_unique(recipe: Recipe):
    if recipe:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, recipe.recipe_nm),
        )


def check_recipe_unreferenced(menu_plan_det_list: list[MenuPlanDet]):
    if menu_plan_det_list:
        menu_plan_example = menu_plan_det_list[0].rel_t_menu_plan.menu_plan_nm
        menu_plan_other = "など" if len(menu_plan_det_list) > 1 else ""
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(
                msg.ME0012_NOT_DELETABLE_FOREIGN_KEY, 
                menu_plan_det_list[0].rel_t_recipe.recipe_nm, 
                "献立プラン", 
                menu_plan_example, 
                menu_plan_other
            ),
        )


def check_recipe_ingred_unique(recipe_ingred: RecipeIngred):
    if recipe_ingred:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(
                msg.ME0013_INGRED_ALREADY_EXISTS, 
                recipe_ingred.rel_t_recipe.recipe_nm, 
                recipe_ingred.rel_m_ingred.ingred_nm,
            ),
        )