from fastapi import HTTPException, status
from app.models import MenuPlan, Recipe, Ingred, RecipeIngred, IngredUnitConv
from app.crud import AppConstCrud
from app.utils import constants as const, message_utils as msg


def check_menu_plan_unique(menu_plan: MenuPlan):
    """献立プラン一意性チェック"""
    if menu_plan:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, menu_plan.menu_plan_nm),
        )


def check_recipe_unique(recipe: Recipe):
    """レシピ一意性チェック"""
    if recipe:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, recipe.recipe_nm),
        )


def check_ingred_unique(ingred: Ingred):
    """食材一意性チェック"""
    if ingred:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, ingred.ingred_nm),
        )


def check_recipe_ingred_unique(recipe_ingred: RecipeIngred):
    """レシピ食材一意性チェック"""
    if recipe_ingred:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(
                msg.ME0013_INGRED_ALREADY_EXISTS, 
                recipe_ingred.rel_t_recipe.recipe_nm, 
                recipe_ingred.rel_m_ingred.ingred_nm,
            ),
        )


def check_ingred_unit_conv_unique(ingred_unit_conv: IngredUnitConv, app_const_crud: AppConstCrud):
    """食材単位変換一意性チェック"""
    if ingred_unit_conv:
        app_const = app_const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred_unit_conv.conv_unit_cd)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0013_DATA_ALREADY_EXISTS_IN_PARENT, ingred_unit_conv.rel_m_ingred.ingred_nm, app_const.val_content),
        ) 