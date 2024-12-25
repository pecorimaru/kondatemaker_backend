from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import IngredUnitConv

class IngredUnitConvDisp(CamelModel):
    ingred_unit_conv_id: int
    ingred_id: int
    conv_unit_cd: str
    conv_rate: float
    conv_weight: Optional[int]=None

    @classmethod
    def from_ingred_unit_conv(cls, ingred_unit_conv: IngredUnitConv):
        return cls(
            ingred_unit_conv_id = ingred_unit_conv.ingred_unit_conv_id, 
            ingred_id = ingred_unit_conv.ingred_id,
            conv_unit_cd = ingred_unit_conv.conv_unit_cd,
            conv_rate = ingred_unit_conv.conv_rate,
        )
