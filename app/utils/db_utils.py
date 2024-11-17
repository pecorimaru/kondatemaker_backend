from datetime import datetime
from typing import Optional


from app.utils.api_utils import CamelModel


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def get_timestamp() -> str:
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

class MenuPlanDisp(CamelModel):
    menu_plan_id: Optional[int]=None
    menu_plan_nm: Optional[str]=None
    menu_plan_nm_k: Optional[str]=None

class MenuPlanDetDisp(CamelModel):
    menu_plan_det_id: int
    menu_plan_id: int
    weekday_cd: str
    recipe_id: int
    recipe_nm: str