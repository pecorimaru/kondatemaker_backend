from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import Ingred

class IngredDisp(CamelModel):
    ingred_id: int
    ingred_nm: str
    ingred_nm_k: Optional[str]=None
    parent_ingred_nm: str
    buy_unit_cd: str
    unit_conv_weight: Optional[int]=None
    sales_area_type: str

    @classmethod
    def from_ingred(cls, ingred: Ingred):
        return cls(
            ingred_id = ingred.ingred_id, 
            ingred_nm = ingred.ingred_nm,
            ingred_nm_k = ingred.ingred_nm_k,
            parent_ingred_nm = ingred.parent_ingred_nm,
            buy_unit_cd = ingred.buy_unit_cd,
            sales_area_type = ingred.sales_area_type,
        )


class DefaultSets(CamelModel):
    unit_cd: Optional[str]=None
    sales_area_type: Optional[str]=None

    @classmethod
    def from_ingred(cls, ingred: Ingred):
        return cls(
            unit_cd = ingred.buy_unit_cd,
            sales_area_type = ingred.sales_area_type,
        )