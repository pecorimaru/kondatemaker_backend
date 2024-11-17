from typing import Optional

from app.utils.api_utils import CamelModel
from app.models import Recipe


class RecipeDisp(CamelModel):
    recipe_id: int
    recipe_nm: Optional[str]=None
    recipe_nm_k: Optional[str]=None
    recipe_type: str
    recipe_url: Optional[str]=None
    visibility_flg: str

    @classmethod
    def from_recipe(cls, recipe: Recipe):
        return cls(
            recipe_id = recipe.recipe_id,
            recipe_nm = recipe.recipe_nm,
            recipe_nm_k = recipe.recipe_nm_k,
            recipe_type = recipe.recipe_type,
            recipe_url = recipe.recipe_url,
            visibility_flg = recipe.visibility_flg,
        )
