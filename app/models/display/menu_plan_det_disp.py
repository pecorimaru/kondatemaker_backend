from app.utils.api_utils import CamelModel
from app.models import MenuPlanDet


class MenuPlanDetDisp(CamelModel):
    menu_plan_det_id: int
    menu_plan_id: int
    weekday_cd: str
    recipe_id: int
    recipe_nm: str

    @classmethod
    def from_menu_plan_det(cls, menu_plan_det: MenuPlanDet):
        return cls(
            menu_plan_det_id = menu_plan_det.menu_plan_det_id,
            menu_plan_id = menu_plan_det.menu_plan_id,
            weekday_cd = menu_plan_det.weekday_cd,
            recipe_id = menu_plan_det.recipe_id,
            recipe_nm = menu_plan_det.rel_t_recipe.recipe_nm,
        )
