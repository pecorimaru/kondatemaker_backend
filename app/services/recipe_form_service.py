from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import RecipeCrud


class RecipeFormService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def fetch_recipe_nm_suggestions(self, input_value: str):
        
        try:
            if not (input_value):
                return []
            
            recipe_crud = RecipeCrud(self.user_id, self.db)
            recipe_nm_suggestions = recipe_crud.get_recipe_nm_suggestions(input_value)    
            return recipe_nm_suggestions

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))

