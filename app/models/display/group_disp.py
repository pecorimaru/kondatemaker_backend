from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import Group, GroupConfig


class GroupDisp(CamelModel):
    group_id: int
    group_nm: str
    current_flg: str
    has_ownership: Optional[str]=None

class GroupMemberDisp(CamelModel):
    user_nm: str
    owner_flg: str

    # @classmethod
    # def from_group(cls, group: Group):
    #     return cls(
    #         # buy_ingred_id = buy_ingred.buy_ingred_id,
    #         # ingred_nm = buy_ingred.ingred_nm,
    #         # qty = buy_ingred.qty,
    #         # unit_cd = buy_ingred.unit_cd,
    #         # sales_area_type = buy_ingred.sales_area_type,
    #         # sales_area_seq = buy_ingred.sales_area_seq,
    #         # manual_add_flg = buy_ingred.manual_add_flg,
    #         # bought_flg = buy_ingred.bought_flg,
    #         # fix_buy_flg = buy_ingred.fix_buy_flg,
    #     )
