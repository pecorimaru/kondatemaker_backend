from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import RecipeCrud, IngredCrud
from app.models.display import RecipeDisp, RecipeIngredDisp

from app.utils import message_utils


class RecipeService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def fetch_recipe_list(self):

        try:
            recipe_crud = RecipeCrud(self.user_id, self.db)
            recipe_list = recipe_crud.get_recipe_list()

            recipe_list_disp = []
            for recipe in recipe_list:    
                recipe_list_disp.append(RecipeDisp.from_recipe(recipe))
            return recipe_list_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_recipe(self, recipe_nm: str, recipe_nm_k: str, recipe_type: str, recipe_url: str) -> RecipeDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.db)
            new_recipe = recipe_crud.create_recipe(recipe_nm, recipe_nm_k, recipe_type, recipe_url)
            return RecipeDisp.from_recipe(new_recipe)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_recipe(self, recipe_id: int, recipe_nm: str, recipe_nm_k: str, recipe_type: str, recipe_url: str) -> RecipeDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.db)
            new_recipe = recipe_crud.update_recipe(recipe_id, recipe_nm, recipe_nm_k, recipe_type, recipe_url)
            return RecipeDisp.from_recipe(new_recipe)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe(self, recipe_id: int) -> RecipeDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.db)
            recipe_crud.delete_recipe(recipe_id)

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_recipe_ingred_list(self, recipe_id: int):

        try:
            recipe_crud = RecipeCrud(None, self.db)
            recipe_ingred_list = recipe_crud.get_recipe_ingred_list(recipe_id)

            recipe_ingred_list_disp = []
            for recipe_ingred in recipe_ingred_list:
                recipe_ingred_list_disp.append(RecipeIngredDisp.from_recipe_ingred(recipe_ingred))

            return recipe_ingred_list_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_recipe_ingred(self, recipe_id: int, ingred_nm: str, qty: float, unit_cd: str) -> RecipeIngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)

            if ingred is None:
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = message_utils.get_message("MW0001", ingred_nm),
                )

            recipe_crud = RecipeCrud(self.user_id, self.db)
            new_recipe_ingred = recipe_crud.create_recipe_ingred(recipe_id, qty, unit_cd, ingred)

            return RecipeIngredDisp.from_recipe_ingred(new_recipe_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_recipe_ingred(self, recipe_ingred_id: int, ingred_nm: str, qty: float, unit_cd: str) -> RecipeIngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)

            if ingred is None:
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = message_utils.get_message("MW0001", ingred_nm),
                )

            recipe_crud = RecipeCrud(self.user_id, self.db)
            new_recipe_ingred = recipe_crud.update_recipe_ingred(recipe_ingred_id, qty, unit_cd, ingred)

            return RecipeIngredDisp.from_recipe_ingred(new_recipe_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe_ingred(self, recipe_ingred_id: int):

        try:
            recipe_crud = RecipeCrud(None, self.db)
            recipe_crud.delete_recipe_ingred(recipe_ingred_id)

            return 

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


