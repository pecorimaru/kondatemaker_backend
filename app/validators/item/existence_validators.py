from fastapi import HTTPException, status
from app.models import MenuPlan, Recipe, Ingred, User
from app.utils import message_utils as msg


def check_menu_plan_exists(menu_plan: MenuPlan, menu_plan_nm: str):
    """献立プラン存在チェック"""
    if not menu_plan:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "献立プラン", menu_plan_nm),
        )


def check_recipe_exists(recipe: Recipe, recipe_nm: str):
    """レシピ存在チェック"""
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "レシピ", recipe_nm),
        )


def check_ingred_exists(ingred: Ingred, ingred_nm: str):
    """食材存在チェック"""
    if not ingred:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "食材", ingred_nm),
        )


def exist_account(user: User):
    """アカウント存在チェック"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=msg.get_message(msg.ME0004_ACCOUNT_NOT_EXISTS),
        ) 