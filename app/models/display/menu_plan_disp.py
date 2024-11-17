from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import MenuPlan


class MenuPlanDisp(CamelModel):
    menu_plan_id: int
    menu_plan_nm: str
    menu_plan_nm_k: Optional[str]

    @classmethod
    def from_menu_plan(cls, menu_plan: MenuPlan):
        return cls(
            menu_plan_id = menu_plan.menu_plan_id,
            menu_plan_nm = menu_plan.menu_plan_nm,
            menu_plan_nm_k = menu_plan.menu_plan_nm_k,
        )
