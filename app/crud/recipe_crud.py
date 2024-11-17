from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.models import Ingred, Recipe, RecipeIngred

from app.utils import db_utils


class RecipeCrud(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def get_recipe(self, recipe_id: int) -> Recipe:

        try:
            recipe = self.db.query(Recipe).filter(Recipe.recipe_id == recipe_id).one()
            return recipe

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_recipe_list(self) -> list[Recipe]:

        try:
            recipe_list = self.db.query(Recipe).filter(Recipe.owner_id == self.user_id).all()
            return recipe_list           

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_recipe_from_nm(self, recipe_nm: str) -> Recipe:

        try:
            recipe = self.db.query(Recipe).filter(Recipe.recipe_nm == recipe_nm, Recipe.owner_id == self.user_id).one()
            return recipe           

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_recipe_nm_suggestions(self, input_value: str) -> list[Recipe]:

        try:
            recipe_nm_suggestions = \
                self.db.query(Recipe.recipe_nm) \
                    .filter(
                        or_(
                        Recipe.recipe_nm.like(f"%{input_value}%"),
                        Recipe.recipe_nm_k.like(f"%{input_value}%")
                        ), 
                        Recipe.owner_id == self.user_id) \
                    .order_by(Recipe.recipe_nm_k).all()

            # SQLAlchemyでは１項目のみで取得してもタプル型リスト[(Recipe.recipe_nm, ),...]になるため
            # str型リスト[(Recipe.recipe_nm),...]に変換する
            return [name[0] for name in recipe_nm_suggestions] if recipe_nm_suggestions else []

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_recipe(self, recipe_nm: str, recipe_nm_k: str, recipe_type: str, recipe_url: str) -> Recipe:

        time_stamp = db_utils.get_timestamp()

        try:
            new_recipe = Recipe(
                recipe_nm = recipe_nm,
                recipe_nm_k = recipe_nm_k,
                recipe_type = recipe_type,
                owner_id = self.user_id,
                recipe_url = recipe_url,
                visibility_flg = "F",
                crt_at = time_stamp,
                upd_at = time_stamp,
                crt_by = self.user_id,
                upd_by = self.user_id,
                version = 0
            )

            self.db.add(new_recipe)
            self.db.commit()
            return new_recipe

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_recipe(self, recipe_id: int, recipe_nm: str, recipe_nm_kana: str, recipe_type: str, recipe_url: str):

        time_stamp = db_utils.get_timestamp()

        try:
            edit_recipe = self.db.query(Recipe).filter(Recipe.recipe_id == recipe_id, Recipe.owner_id == self.user_id).one()
            edit_recipe.recipe_nm = recipe_nm
            edit_recipe.recipe_nm_k = recipe_nm_kana
            edit_recipe.recipe_type = recipe_type
            edit_recipe.recipe_url = recipe_url
            edit_recipe.upd_at = time_stamp
            edit_recipe.upd_by = self.user_id
            edit_recipe.version = edit_recipe.version + 1

            self.db.commit()
            return edit_recipe

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe(self, recipe_id: int):

        try:
            self.db.query(Recipe).filter(Recipe.recipe_id == recipe_id, Recipe.owner_id == self.user_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_recipe_ingred_list(self, recipe_id: int) -> list[RecipeIngred]:

        try:
            recipe_ingred_list = self.db.query(RecipeIngred).filter(RecipeIngred.recipe_id == recipe_id).all();
            return recipe_ingred_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_recipe_ingred(self, recipe_id: int, qty: float, unit_cd: str, ingred: Ingred) -> RecipeIngred:

        time_stamp = db_utils.get_timestamp()

        try:
            new_recipe_ingred = RecipeIngred(
                recipe_id = recipe_id,
                ingred_id = ingred.ingred_id,
                qty = qty,
                unit_cd = unit_cd,
                crt_at = time_stamp,
                upd_at = time_stamp,
                crt_by = self.user_id,
                upd_by = self.user_id,
                version = 0
            )

            self.db.add(new_recipe_ingred)
            self.db.commit()
            return new_recipe_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_recipe_ingred(self, recipe_ingred_id: int, qty: float, unit_cd: str, ingred: Ingred) -> RecipeIngred:

        time_stamp = db_utils.get_timestamp()

        try:
            edit_recipe_ingred = self.db.query(RecipeIngred).filter(RecipeIngred.recipe_ingred_id == recipe_ingred_id).one()
            edit_recipe_ingred.ingred_id = ingred.ingred_id
            edit_recipe_ingred.qty = qty
            edit_recipe_ingred.unit_cd = unit_cd
            edit_recipe_ingred.upd_at = time_stamp
            edit_recipe_ingred.upd_by = self.user_id
            edit_recipe_ingred.version = edit_recipe_ingred.version + 1

            self.db.commit()
            return edit_recipe_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_recipe_ingred(self, recipe_ingred_id: int):

        try:
            self.db.query(RecipeIngred).filter(RecipeIngred.recipe_ingred_id == recipe_ingred_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    # def cnv_model_to_recipe_disp(self, recipe: Recipe) -> RecipeDisp:

    #     return RecipeDisp(
    #         recipe_id = recipe.recipe_id,
    #         recipe_nm = recipe.recipe_nm,
    #         recipe_nm_k = recipe.recipe_nm_k,
    #         recipe_type = recipe.recipe_type,
    #         recipe_url = recipe.recipe_url,
    #         visibility_flg = recipe.visibility_flg,
    #     )


    # def cnv_model_to_recipe_ingred_disp(self, recipe_ingred: RecipeIngred) -> RecipeIngredDisp:

    #     return RecipeIngredDisp(
    #         recipe_id = recipe_ingred.recipe_id,
    #         recipe_ingred_id = recipe_ingred.recipe_ingred_id,
    #         ingred_nm = recipe_ingred.rel_m_ingred.ingred_nm,
    #         qty = recipe_ingred.qty,
    #         unit_cd = recipe_ingred.unit_cd,
    #         sales_area_type = recipe_ingred.rel_m_ingred.sales_area_type
    #     )