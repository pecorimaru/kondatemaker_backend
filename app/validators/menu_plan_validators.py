from fastapi import HTTPException, status

from app.models import MenuPlan
from app.utils import message_utils as msg


def check_menu_plan_exists(menu_plan: MenuPlan, menu_plan_nm: str):
    if not menu_plan:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "献立プラン", menu_plan_nm),
        )


def check_menu_plan_unique(menu_plan: MenuPlan):
    if menu_plan:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0014_DATA_ALREADY_EXISTS, menu_plan.menu_plan_nm),
        )


