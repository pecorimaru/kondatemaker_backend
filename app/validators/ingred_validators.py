from fastapi import HTTPException, status

from app.models import Ingred, IngredUnitConv, RecipeIngred
from app.crud import AppConstCrud
from app.utils import constants as const, message_utils as msg


def check_ingred_exists(ingred: Ingred, ingred_nm: str):
    if not ingred:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "食材", ingred_nm),
        )


def check_ingred_unique(ingred: Ingred):
    if ingred:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, ingred.ingred_nm),
        )


def check_ingred_unreferenced(recipe_ingred_list: list[RecipeIngred]):
    # 削除対象のレシピが献立明細に参照されていた場合
    if recipe_ingred_list:
        recipe_example = recipe_ingred_list[0].rel_t_recipe.recipe_nm
        recipe_other = "など" if len(recipe_ingred_list) > 1 else ""
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(
                msg.ME0012_NOT_DELETABLE_FOREIGN_KEY, 
                recipe_ingred_list[0].rel_m_ingred.ingred_nm, 
                "レシピ", 
                recipe_example, 
                recipe_other
            ),
        )


def check_ingred_unit_conv_unique(ingred_unit_conv: IngredUnitConv, app_const_crud: AppConstCrud):
    if ingred_unit_conv:
        app_const = app_const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred_unit_conv.conv_unit_cd)
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0013_DATA_ALREADY_EXISTS_IN_PARENT, ingred_unit_conv.rel_m_ingred.ingred_nm, app_const.val_content),
        )