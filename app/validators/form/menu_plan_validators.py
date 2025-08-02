from app.models import Recipe
from app.validators.item import check_recipe_exists, check_weekday_cd

def menu_plan_det_form_validate(weekday_cd: str, recipe: Recipe, recipe_nm: str):
    check_weekday_cd(weekday_cd)
    check_recipe_exists(recipe, recipe_nm)