from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import UserCrud, RecipeCrud, MenuPlanCrud, WorkCrud, AppConstCrud
from app.models.display import MenuPlanDisp, ToweekMenuPlanDetDisp

from app.utils import constants as const


class HomeService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_selected_plan(self) -> MenuPlanDisp:

        try:
            # 前回指定した献立プランIDを取得
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_id = user_crud.get_toweek_menu_plan_id()

            # 前回の指定がない場合は終了
            if not menu_plan_id:
                return MenuPlanDisp(
                    menu_plan_id = None,
                    menu_plan_nm = "未選択",
                    menu_plan_nm_k = None
                )
            
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan = menu_plan_crud.get_menu_plan(menu_plan_id)

            if not menu_plan:
                return MenuPlanDisp(
                    menu_plan_id = None,
                    menu_plan_nm = "削除されました",
                    menu_plan_nm_k = None
                )

            return MenuPlanDisp.from_menu_plan(menu_plan)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_toweek_menu_plan_det(self) -> dict[str, list]:

        try:
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            toweek_menu_plan_det_list = work_crud.get_toweek_menu_plan_det_list()

            # 今週献立明細リストを明細ごとに曜日をキーとした辞書変数にセット
            toweek_menu_plan_det_list_dict = self.cnv_menu_plan_det_list_map_to_weekday_dict(toweek_menu_plan_det_list)
            return toweek_menu_plan_det_list_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def recreate_toweek_plan(self, selected_plan_id: int) -> dict[str, list]:

        try:
            # 既存のワークデータを削除
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            work_crud.delete_toweek_menu_plan_det_all()
            work_crud.delete_buy_ingred_other_than_fix_buy()
            work_crud.reset_buy_ingred_fix_buy_flg()

            # 指定した献立プランをユーザー設定に登録
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user_crud.update_toweek_menu_plan(selected_plan_id)

            # 指定した献立プランに紐付く献立明細を取得
            menu_plan_crud = MenuPlanCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            menu_plan_det_list = menu_plan_crud.get_menu_plan_det_list(selected_plan_id)

            # ワークデータを登録
            new_toweek_menu_plan_det_list = work_crud.create_toweek_menu_plan_det_list(menu_plan_det_list)
            work_crud.create_buy_ingred_from_selected_plan()

            self.db.commit()

            # 今週献立明細リストを明細ごとに曜日をキーとした辞書変数にセット
            new_toweek_menu_plan_det_list_dict = self.cnv_menu_plan_det_list_map_to_weekday_dict(new_toweek_menu_plan_det_list)
            return new_toweek_menu_plan_det_list_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def cnv_menu_plan_det_list_map_to_weekday_dict(self, menu_plan_det_list) -> dict[str, list]:

        try: 
            menu_plan_det_list_dict = {}

            # 曜日ごとにループ
            const_crud = AppConstCrud(self.db)
            weekday_list = const_crud.get_app_consts(const.APP_CONST_C0005_WEEKDAY_TYPE)
            for weekday in weekday_list:
                weekday_menu_plan_det_list = []

                # 曜日の合致する献立明細をリストに追加
                for menu_plan_det in menu_plan_det_list:    
                    if weekday.val == menu_plan_det.weekday_cd:
                        weekday_menu_plan_det_list.append(ToweekMenuPlanDetDisp.from_toweek_menu_plan_det(menu_plan_det)
                )
                menu_plan_det_list_dict[weekday.val] = weekday_menu_plan_det_list

            return menu_plan_det_list_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_toweek_menu_plan_det(self, recipe_nm: str, weekday_cd: str) -> ToweekMenuPlanDetDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe = recipe_crud.get_recipe_from_nm(recipe_nm)

            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_toweek_menu_plan_det = work_crud.create_toweek_menu_plan_det(recipe.recipe_id, weekday_cd)

            # 追加するレシピの食材を購入食材に追加 or 必要量更新
            work_crud.sum_buy_ingred_from_recipe(recipe)

            self.db.commit()

            # 最新の今週献立明細リストを取得
            toweek_menu_plan_det_list = work_crud.get_toweek_menu_plan_det_list()
            toweek_menu_plan_det_list_dict = self.cnv_menu_plan_det_list_map_to_weekday_dict(toweek_menu_plan_det_list)
            return toweek_menu_plan_det_list_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_toweek_menu_plan_det(self, toweek_menu_plan_det_id: int, recipe_nm: str) -> ToweekMenuPlanDetDisp:

        try:
            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_recipe = recipe_crud.get_recipe_from_nm(recipe_nm)

            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            bef_toweek_menu_plan_det = work_crud.get_toweek_menu_plan_det(toweek_menu_plan_det_id)
            bef_recipe = recipe_crud.get_recipe(bef_toweek_menu_plan_det.recipe_id)

            edit_toweek_menu_plan_det = work_crud.update_toweek_menu_plan_det(toweek_menu_plan_det_id, new_recipe.recipe_id)

            # 更新前レシピの食材を購入食材から削除 or 必要量更新
            work_crud.reduce_buy_ingred_from_recipe(bef_recipe)

            # 更新後レシピの食材を購入食材に追加 or 必要量更新
            work_crud.sum_buy_ingred_from_recipe(new_recipe)

            self.db.commit()
            
            # 最新の今週献立明細リストを取得
            toweek_menu_plan_det_list = work_crud.get_toweek_menu_plan_det_list()
            toweek_menu_plan_det_list_dict = self.cnv_menu_plan_det_list_map_to_weekday_dict(toweek_menu_plan_det_list)
            return toweek_menu_plan_det_list_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_toweek_menu_plan_det(self, toweek_menu_plan_det_id: int):

        try:
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            toweek_menu_plan_det = work_crud.get_toweek_menu_plan_det(toweek_menu_plan_det_id)

            recipe_crud = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe = recipe_crud.get_recipe(toweek_menu_plan_det.recipe_id)

            work_crud.delete_toweek_menu_plan_det(toweek_menu_plan_det_id)

            # 削除するレシピの食材を購入食材から削除 or 必要量更新
            work_crud.reduce_buy_ingred_from_recipe(recipe)

            self.db.commit()

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


