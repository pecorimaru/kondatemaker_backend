from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import RecipeIngred


class RecipeIngredDisp(CamelModel):
    recipe_ingred_id: int
    recipe_id: int
    ingred_nm: str
    qty: float
    unit_cd: str
    sales_area_type: Optional[str]=None

    @classmethod
    def from_recipe_ingred(cls, recipe_ingred: RecipeIngred):
        return cls(
            recipe_ingred_id = recipe_ingred.recipe_ingred_id,
            recipe_id = recipe_ingred.recipe_id,
            ingred_nm = recipe_ingred.rel_m_ingred.ingred_nm,
            qty = recipe_ingred.qty,
            unit_cd = recipe_ingred.unit_cd,
            sales_area_type = recipe_ingred.rel_m_ingred.sales_area_type,
        )
