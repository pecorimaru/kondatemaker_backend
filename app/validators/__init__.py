# 後方互換性のため、以前のインポート形式をサポート
from app.validators.item import (
    # 存在チェック系
    check_menu_plan_exists,
    check_recipe_exists,
    check_ingred_exists,
    exist_account,
    
    # 一意性チェック系
    check_menu_plan_unique,
    check_recipe_unique,
    check_ingred_unique,
    check_recipe_ingred_unique,
    check_ingred_unit_conv_unique,
    
    # 参照整合性チェック系
    check_recipe_unreferenced,
    check_ingred_unreferenced,
    
    # ビジネスルール系
    check_weekday_cd,
    verify_password,
    ensure_not_deleted,
    ensure_deleted,
    ensure_activate,
    ensure_alive_token
)

# 既存のコードとの互換性のために旧形式のモジュール構造をエミュレート
class MenuPlanValidators:
    check_menu_plan_exists = staticmethod(check_menu_plan_exists)
    check_menu_plan_unique = staticmethod(check_menu_plan_unique)
    check_weekday_cd = staticmethod(check_weekday_cd)

class RecipeValidators:
    check_recipe_exists = staticmethod(check_recipe_exists)
    check_recipe_unique = staticmethod(check_recipe_unique)
    check_recipe_unreferenced = staticmethod(check_recipe_unreferenced)
    check_recipe_ingred_unique = staticmethod(check_recipe_ingred_unique)

class IngredValidators:
    check_ingred_exists = staticmethod(check_ingred_exists)
    check_ingred_unique = staticmethod(check_ingred_unique)
    check_ingred_unreferenced = staticmethod(check_ingred_unreferenced)
    check_ingred_unit_conv_unique = staticmethod(check_ingred_unit_conv_unique)

class UserValidators:
    verify_password = staticmethod(verify_password)
    ensure_not_deleted = staticmethod(ensure_not_deleted)
    ensure_deleted = staticmethod(ensure_deleted)
    ensure_activate = staticmethod(ensure_activate)
    ensure_alive_token = staticmethod(ensure_alive_token)
    exist_account = staticmethod(exist_account)

# 旧形式のインポートをサポート
menu_plan_validators = MenuPlanValidators()
recipe_validators = RecipeValidators()
ingred_validators = IngredValidators()
user_validators = UserValidators() 