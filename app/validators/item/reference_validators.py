from fastapi import HTTPException, status
from app.models import MenuPlanDet, RecipeIngred
from app.utils import message_utils as msg


def check_recipe_unreferenced(menu_plan_det_list: list[MenuPlanDet]):
    """レシピ非参照チェック"""
    if menu_plan_det_list:
        menu_plan_example = menu_plan_det_list[0].rel_t_menu_plan.menu_plan_nm
        menu_plan_other = "など" if len(menu_plan_det_list) > 1 else ""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(
                msg.ME0012_NOT_DELETABLE_FOREIGN_KEY, 
                menu_plan_det_list[0].rel_t_recipe.recipe_nm, 
                "献立プラン", 
                menu_plan_example, 
                menu_plan_other
            ),
        )


def check_ingred_unreferenced(recipe_ingred_list: list[RecipeIngred]):
    """食材非参照チェック"""
    if recipe_ingred_list:
        recipe_example = recipe_ingred_list[0].rel_t_recipe.recipe_nm
        recipe_other = "など" if len(recipe_ingred_list) > 1 else ""
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(
                msg.ME0012_NOT_DELETABLE_FOREIGN_KEY, 
                recipe_ingred_list[0].rel_m_ingred.ingred_nm, 
                "レシピ", 
                recipe_example, 
                recipe_other
            ),
        ) 