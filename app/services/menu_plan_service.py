from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.models.display import MenuPlanDisp, MenuPlanDetDisp
from app.crud import MenuPlanCrud, RecipeCrud
from app.validators import recipe_validators


class MenuPlanService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_menu_plan_list(self) -> list[MenuPlanDisp]:

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_list = menu_plan_crud.get_menu_plan_list()

            menu_plan_disp_list = []
            for menu_plan in menu_plan_list:
                menu_plan_disp_list.append(MenuPlanDisp.from_menu_plan(menu_plan))

            return menu_plan_disp_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_menu_plan_det_list(self, menu_plan_id: int):

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_det_list = menu_plan_crud.get_menu_plan_det_list(menu_plan_id)

            menu_plan_det_disp_list = []
            for menu_plan_det in menu_plan_det_list:
                menu_plan_det_disp_list.append(MenuPlanDetDisp.from_menu_plan_det(menu_plan_det))

            return menu_plan_det_disp_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_menu_plan(self, menu_plan_nm, menu_plan_nm_k):

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_menu_plan = menu_plan_crud.create_menu_plan(menu_plan_nm, menu_plan_nm_k)

            return MenuPlanDisp.from_menu_plan(new_menu_plan)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_menu_plan(self, menu_plan_id: int, menu_plan_nm: str, menu_plan_nm_k: str):

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_menu_plan = menu_plan_crud.update_menu_plan(menu_plan_id, menu_plan_nm, menu_plan_nm_k)

            return MenuPlanDisp.from_menu_plan(new_menu_plan)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_menu_plan(self, menu_plan_id: int):

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_crud.delete_menu_plan_det_from_menu_plan(menu_plan_id)
            menu_plan_crud.delete_menu_plan(menu_plan_id)

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_menu_plan_det(self, menu_plan_id: int, weekday_cd: str, recipe_nm: str):

        try:
            # 入力したレシピが存在しない場合
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe = recipe_crud.get_recipe_from_nm(recipe_nm)
            recipe_validators.exist_recipe(recipe, recipe_nm)

            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_menu_plan_det = menu_plan_crud.create_menu_plan_det(menu_plan_id, weekday_cd, recipe_nm)

            return MenuPlanDetDisp.from_menu_plan_det(new_menu_plan_det)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_menu_plan_det(self, menu_plan_det_id: int, weekday_cd: str, recipe_nm: str):

        try:
            # 入力したレシピが存在しない場合
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe = recipe_crud.get_recipe_from_nm(recipe_nm)
            recipe_validators.exist_recipe(recipe, recipe_nm)

            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_menu_plan_det = menu_plan_crud.update_menu_plan_det(menu_plan_det_id, weekday_cd, recipe_nm)

            return MenuPlanDetDisp.from_menu_plan_det(new_menu_plan_det)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
        

    def delete_menu_plan_det(self, menu_plan_det_id: int):

        try:
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_crud.delete_menu_plan_det(menu_plan_det_id)

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))