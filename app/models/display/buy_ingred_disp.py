from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import BuyIngred


class BuyIngredDisp(CamelModel):
    buy_ingred_id: int
    ingred_nm: str
    qty: Optional[float]=None
    unit_cd: str
    sales_area_type: str
    sales_area_seq: Optional[int]
    manual_add_flg: str
    bought_flg: str
    fix_buy_flg: str

    @classmethod
    def from_buy_ingred(cls, buy_ingred: BuyIngred):
        return cls(
            buy_ingred_id = buy_ingred.buy_ingred_id,
            ingred_nm = buy_ingred.ingred_nm,
            qty = buy_ingred.qty,
            unit_cd = buy_ingred.unit_cd,
            sales_area_type = buy_ingred.sales_area_type,
            sales_area_seq = buy_ingred.sales_area_seq,
            manual_add_flg = buy_ingred.manual_add_flg,
            bought_flg = buy_ingred.bought_flg,
            fix_buy_flg = buy_ingred.fix_buy_flg,
        )
