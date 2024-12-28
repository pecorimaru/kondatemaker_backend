from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.base_service import BaseService
from app.models import Recipe, MenuPlan, MenuPlanDet

from app.utils import db_utils


class MenuPlanCrud(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def get_menu_plan(self, menu_plan_id: int) -> MenuPlan:

        try:
            menu_plan = self.db.query(MenuPlan).filter(MenuPlan.menu_plan_id == menu_plan_id).one_or_none()
            return menu_plan

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_menu_plan_from_nm(self, menu_plan_nm: str) -> MenuPlan:

        try:
            menu_plan = self.db.query(MenuPlan).filter(MenuPlan.menu_plan_nm == menu_plan_nm, MenuPlan.owner_user_id == self.owner_user_id).one()
            return menu_plan

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_menu_plan_list(self) -> list[MenuPlan]:

        try:
            menu_plan_list = self.db.query(MenuPlan).filter(MenuPlan.owner_user_id == self.owner_user_id).order_by(MenuPlan.menu_plan_nm_k, MenuPlan.menu_plan_nm).all()
            if menu_plan_list:
                return menu_plan_list
            return []

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_menu_plan_det_list(self, menu_plan_id: str) -> list[MenuPlanDet]:

        try:
            menu_plan_det_list = self.db.query(MenuPlanDet).filter(MenuPlanDet.menu_plan_id == menu_plan_id).order_by(MenuPlanDet.weekday_cd).all()
            if menu_plan_det_list:
                return menu_plan_det_list
            return []

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_menu_plan_det_list_from_recipe_id(self, recipe_id: int) -> list[MenuPlanDet]:

        try:
            menu_plan_det_list = self.db.query(MenuPlanDet).filter(MenuPlanDet.recipe_id == recipe_id).all()
            return menu_plan_det_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_menu_plan(self, menu_plan_nm: str, menu_plan_nm_k: str) -> MenuPlan:

        time_stamp = db_utils.get_timestamp()

        try:
            new_menu_plan = MenuPlan(
                menu_plan_nm = menu_plan_nm,
                menu_plan_nm_k = menu_plan_nm_k,
                owner_user_id = self.owner_user_id,
                visibility_flg = 'F',
                crt_timestamp = time_stamp,
                upd_timestamp = time_stamp,
                crt_user_id = self.user_id,
                upd_user_id = self.user_id,
                version = 0
            )

            self.db.add(new_menu_plan)
            self.db.flush()

            return new_menu_plan

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_menu_plan(self, menu_plan_id: int, menu_plan_nm: str, menu_plan_nm_k: str) -> MenuPlan:

        time_stamp = db_utils.get_timestamp()

        try:
            edit_menu_plan = self.db.query(MenuPlan).filter(MenuPlan.menu_plan_id == menu_plan_id).one()
            edit_menu_plan.menu_plan_nm = menu_plan_nm
            edit_menu_plan.menu_plan_nm_k = menu_plan_nm_k
            edit_menu_plan.upd_timestamp = time_stamp
            edit_menu_plan.upd_user_id = self.user_id
            edit_menu_plan.version = edit_menu_plan.version + 1

            return edit_menu_plan


        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_menu_plan(self, menu_plan_id: int):

        try:
            self.db.query(MenuPlan).filter(MenuPlan.menu_plan_id == menu_plan_id).delete()

            return
            
        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_menu_plan_all(self):

        try:
            self.db.query(MenuPlan).filter(MenuPlan.owner_user_id == self.owner_user_id).delete()

            return
            
        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
            

    def create_menu_plan_det(self, menu_plan_id: str, weekday_cd: str, recipe_nm: str) -> MenuPlanDet:

        time_stamp = db_utils.get_timestamp()

        try:
            recipe = self.db.query(Recipe).filter(Recipe.recipe_nm == recipe_nm, Recipe.owner_user_id == self.owner_user_id).one()

            new_menu_plan_det = MenuPlanDet(
                menu_plan_id = menu_plan_id,
                weekday_cd = weekday_cd,
                recipe_id = recipe.recipe_id,
                crt_timestamp = time_stamp,
                upd_timestamp = time_stamp,
                crt_user_id = self.user_id,
                upd_user_id = self.user_id,
                version = 0
            )

            self.db.add(new_menu_plan_det)
            self.db.flush()

            return new_menu_plan_det

        except SQLAlchemyError as e:
            self.db.rollback() 
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_menu_plan_det(self, menu_plan_det_id: str, weekday_cd: str, recipe_nm: str) -> MenuPlanDet:

        time_stamp = db_utils.get_timestamp()

        try:
            recipe = self.db.query(Recipe).filter(Recipe.recipe_nm == recipe_nm, Recipe.owner_user_id == self.owner_user_id).one()
            edit_menu_plan_det = self.db.query(MenuPlanDet).filter(MenuPlanDet.menu_plan_det_id == menu_plan_det_id).one()
            edit_menu_plan_det.weekday_cd = weekday_cd
            edit_menu_plan_det.recipe_id = recipe.recipe_id
            edit_menu_plan_det.upd_timestamp = time_stamp
            edit_menu_plan_det.upd_user_id = self.user_id
            edit_menu_plan_det.version = edit_menu_plan_det.version + 1

            return edit_menu_plan_det

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_menu_plan_det(self, menu_plan_det_id: int):

        try:
            self.db.query(MenuPlanDet).filter(MenuPlanDet.menu_plan_det_id == menu_plan_det_id).delete()

            return 

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_menu_plan_det_from_menu_plan(self, menu_plan_id: int):

        try:
            self.db.query(MenuPlanDet).filter(MenuPlanDet.menu_plan_id == menu_plan_id).delete()

            return 

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
