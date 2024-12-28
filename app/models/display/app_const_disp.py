from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import AppConst


class AppConstDisp(CamelModel):
    val: str
    val_content: str
    sort_seq: int
    generic_item1: str
    generic_item2: Optional[str]=None

    @classmethod
    def from_app_const(cls, app_const: AppConst):
        return cls(
            val = app_const.val,
            val_content = app_const.val_content,
            sort_seq = app_const.sort_seq,
            generic_item1 = app_const.generic_item1,
            generic_item2 = app_const.generic_item2,
        )