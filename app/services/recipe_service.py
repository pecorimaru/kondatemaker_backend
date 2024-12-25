from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import RecipeCrud, IngredCrud
from app.models.display import RecipeDisp, RecipeIngredDisp
from app.validators import recipe_validators, ingred_validators

from app.utils import message_utils as msg


class RecipeService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_recipe_list(self):

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
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
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            recipe = recipe_crud.get_recipe_from_nm(recipe_nm)
            recipe_validators.recipe_not_duplicate(recipe, recipe_nm)
            
            new_recipe = recipe_crud.create_recipe(recipe_nm, recipe_nm_k, recipe_type, recipe_url)
            self.db.commit()

            return RecipeDisp.from_recipe(new_recipe)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_recipe(self, recipe_id: int, recipe_nm: str, recipe_nm_k: str, recipe_type: str, recipe_url: str) -> RecipeDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            recipe = recipe_crud.get_recipe_from_nm(recipe_nm)
            recipe_validators.recipe_not_duplicate(recipe, recipe_nm)

            new_recipe = recipe_crud.update_recipe(recipe_id, recipe_nm, recipe_nm_k, recipe_type, recipe_url)
            self.db.commit()

            return RecipeDisp.from_recipe(new_recipe)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe(self, recipe_id: int) -> RecipeDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            # 削除対象のレシピが献立明細に参照されていた場合
            menu_plan_det_list = recipe_crud.delete_recipe(recipe_id)
            recipe_validators.recipe_not_referenced(menu_plan_det_list, recipe_crud, recipe_id)

            self.db.commit()

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_recipe_ingred_list(self, recipe_id: int):

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
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
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)

            # 入力した食材が存在しない場合
            ingred_validators.exist_ingred(ingred, ingred_nm)

            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            # 同名の食材が既に登録されている場合
            recipe_ingred = recipe_crud.get_recipe_ingred_from_ingred(recipe_id, ingred.ingred_id)
            recipe_validators.ingred_not_duplicate(recipe_ingred, ingred_nm)
                
            new_recipe_ingred = recipe_crud.create_recipe_ingred(recipe_id, qty, unit_cd, ingred)
            self.db.commit()

            return RecipeIngredDisp.from_recipe_ingred(new_recipe_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_recipe_ingred(self, recipe_ingred_id: int, ingred_nm: str, qty: float, unit_cd: str) -> RecipeIngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)

            # 入力した食材が存在しない場合
            ingred_validators.exist_ingred(ingred, ingred_nm)

            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            # 同名の食材が既に登録されている場合
            current_recipe_ingred = recipe_crud.get_recipe_ingred(recipe_ingred_id)
            recipe_ingred = recipe_crud.get_recipe_ingred_from_ingred(current_recipe_ingred.rel_t_recipe.recipe_id, ingred.ingred_id)
            recipe_validators.ingred_not_duplicate(recipe_ingred, ingred_nm)
            
            new_recipe_ingred = recipe_crud.update_recipe_ingred(recipe_ingred_id, qty, unit_cd, ingred)
            self.db.commit()

            return RecipeIngredDisp.from_recipe_ingred(new_recipe_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe_ingred(self, recipe_ingred_id: int):

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe_crud.delete_recipe_ingred(recipe_ingred_id)
            self.db.commit()

            return 

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


