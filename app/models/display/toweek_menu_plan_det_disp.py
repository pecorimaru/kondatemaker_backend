from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import ToweekMenuPlanDet


class ToweekMenuPlanDetDisp(CamelModel):
    toweek_menu_plan_det_id: int
    weekday_cd: str
    recipe_id: int
    recipe_nm: str
    recipe_url: Optional[str]=None

    @classmethod
    def from_toweek_menu_plan_det(cls, toweek_menu_plan_det: ToweekMenuPlanDet):
        return cls(
            toweek_menu_plan_det_id = toweek_menu_plan_det.toweek_menu_plan_det_id,
            weekday_cd = toweek_menu_plan_det.weekday_cd,
            recipe_id = toweek_menu_plan_det.recipe_id,
            recipe_nm = toweek_menu_plan_det.rel_t_recipe.recipe_nm,
            recipe_url = toweek_menu_plan_det.rel_t_recipe.recipe_url,
        )
