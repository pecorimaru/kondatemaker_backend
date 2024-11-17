from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.base_service import BaseService
from app.models import Recipe, RecipeIngred, MenuPlanDet, BuyIngred, ToweekMenuPlanDet, AppConst

from app.crud.app_const_crud import AppConstCrud
from app.crud.ingred_crud import IngredCrud

from app.utils import db_utils, constants as const


class WorkCrud(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def get_toweek_menu_plan_det(self, toweek_menu_plan_det_id: int) -> ToweekMenuPlanDet:

        try:
            toweek_menu_plan_det = self.db \
                .query(ToweekMenuPlanDet).filter(ToweekMenuPlanDet.toweek_menu_plan_det_id == toweek_menu_plan_det_id).one() 

            return toweek_menu_plan_det

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_toweek_menu_plan_det_list(self) -> list[ToweekMenuPlanDet]:

        try:
            toweek_menu_plan_det_list = self.db \
                .query(ToweekMenuPlanDet) \
                .filter(ToweekMenuPlanDet.owner_user_id == self.user_id) \
                .order_by(ToweekMenuPlanDet.weekday_cd) \
                .all() 

            return toweek_menu_plan_det_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_toweek_menu_plan_det(self, recipe_id: int, weekday_cd: str):

        today = db_utils.get_timestamp()
        new_toweek_menu_plan_det = ToweekMenuPlanDet(
            owner_user_id = self.user_id,
            weekday_cd = weekday_cd,
            recipe_id = recipe_id,
            crt_dt = today
        )

        try:
            self.db.add(new_toweek_menu_plan_det)
            self.db.commit()

            return new_toweek_menu_plan_det

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_toweek_menu_plan_det_list(self, menu_plan_det_list: list[MenuPlanDet]):

        today = db_utils.get_timestamp()

        toweek_menu_plan_det_list = []
        for menu_plan_det in menu_plan_det_list:
            toweek_menu_plan_det_list.append(ToweekMenuPlanDet(
                owner_user_id = self.user_id,
                weekday_cd = menu_plan_det.week_day_cd,
                recipe_id = menu_plan_det.recipe_id,
                crt_dt = today
            ))

        try:
            self.db.add_all(toweek_menu_plan_det_list)
            self.db.commit()

            return toweek_menu_plan_det_list

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_toweek_menu_plan_det(self, toweek_menu_plan_det_id: int, recipe_id: str):

        try:
            edit_toweek_menu_plan_det = self.db \
                .query(ToweekMenuPlanDet) \
                .filter(
                    ToweekMenuPlanDet.toweek_menu_plan_det_id == toweek_menu_plan_det_id,
                    ToweekMenuPlanDet.owner_user_id == self.user_id,
                ).one()

            edit_toweek_menu_plan_det.recipe_id = recipe_id
            self.db.commit()

            return edit_toweek_menu_plan_det

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_toweek_menu_plan_det_all(self):

        try:
            self.db.query(ToweekMenuPlanDet).filter(ToweekMenuPlanDet.owner_user_id == self.user_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_toweek_menu_plan_det(self, toweek_menu_plan_det_id: int):

        try:
            self.db \
                .query(ToweekMenuPlanDet) \
                .filter(
                    ToweekMenuPlanDet.toweek_menu_plan_det_id == toweek_menu_plan_det_id,
                    ToweekMenuPlanDet.owner_user_id == self.user_id,
                ).delete()
            self.db.commit()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_buy_ingred_without_manual_add(self, ingred_nm: str) -> BuyIngred:

        try:
            buy_ingred = self.db \
                .query(BuyIngred) \
                .filter(
                    BuyIngred.ingred_nm == ingred_nm, 
                    BuyIngred.user_id == self.user_id,
                    BuyIngred.manual_add_flg == "F",   # 自動追加された購入食材であれば一意に取得可能
                ).one_or_none()

            return buy_ingred           

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_buy_ingred_list(self) -> list[BuyIngred]:

        try:
            buy_ingred_list = self.db.query(BuyIngred).filter(BuyIngred.user_id == self.user_id).all()

            return buy_ingred_list           

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_buy_ingred(self, ingred_nm: str, qty: float, unit_cd: str, const_sales_area_type: AppConst):

        new_buy_ingred = BuyIngred(
            user_id = self.user_id,
            ingred_nm = ingred_nm,
            qty = qty,
            unit_cd = unit_cd,
            sales_area_type = const_sales_area_type.val,
            sales_area_seq = const_sales_area_type.sort_seq,
            manual_add_flg = "T",
            bought_flg = "F"
        )

        try:
            self.db.add(new_buy_ingred)
            self.db.commit()

            return new_buy_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def sum_buy_ingred_from_recipe(self, recipe: Recipe):

        try:
            const_crud = AppConstCrud(self.db)

            new_buy_ingred_list = []
            for recipe_ingred in recipe.rel_t_recipe_ingred:

                # レシピ食材として利用した単位から購入単位に置き換えて必要量を再計算
                recalc_qty = self.get_recalc_qty(recipe_ingred)

                # レシピ食材と同名の購入食材が存在する場合は取得
                edit_buy_ingred = self.get_buy_ingred_without_manual_add(recipe_ingred.rel_m_ingred.ingred_nm)

                # 同名の購入食材が取得できた場合は更新処理
                if edit_buy_ingred:
                    edit_buy_ingred.qty = edit_buy_ingred.qty + recalc_qty

                # 同名の購入食材が取得できなかった場合は追加処理
                else:
                    const_sales_area_type = const_crud.get_app_const_from_val(const.APP_CONST_C0004_SALES_AREA_TYPE, recipe_ingred.rel_m_ingred.sales_area_type)

                    new_buy_ingred = BuyIngred(
                        user_id = self.user_id,
                        ingred_nm = recipe_ingred.rel_m_ingred.ingred_nm,
                        qty = recalc_qty,
                        unit_cd = recipe_ingred.unit_cd,
                        sales_area_type = recipe_ingred.rel_m_ingred.sales_area_type,
                        sales_area_seq = const_sales_area_type.sort_seq,
                        manual_add_flg = "F",
                        bought_flg = "F"
                    )
                    new_buy_ingred_list.append(new_buy_ingred)
                
            self.db.add_all(new_buy_ingred_list)
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_buy_ingred_from_selected_plan(self):

        sql = text(
            """
            SELECT
                :user_id                     AS user_id
                , t3.ingred_nm                 AS ingred_nm
                , SUM(t2.qty / t4.conv_rate)   AS qty
                , t3.standard_unit_cd          AS unit_cd
                , t3.sales_area_type           AS sales_area_type
                , c0004.sort_seq               AS sales_area_seq
            FROM
                w_toweek_menu_plan_det t1 
                LEFT JOIN t_recipe_ingred t2 
                    ON t1.recipe_id = t2.recipe_id 
                LEFT JOIN m_ingred t3 
                    ON t2.ingred_id = t3.ingred_id 
                LEFT JOIN m_ingred_unit_conv t4 
                    ON t4.ingred_id = t2.ingred_id 
                    AND t4.from_unit_cd = t2.unit_cd 
                LEFT JOIN c_app_const c0004
                    ON c0004.type_cd = 'C0004'
                    AND c0004.val = t3.sales_area_type
            WHERE
                t1.owner_user_id = :user_id
                AND t2.recipe_ingred_id IS NOT NULL 
            GROUP BY
                t3.ingred_nm
            ORDER BY c0004.sort_seq
            """
        )

        try:
            result = self.db.execute(sql, {"user_id": self.user_id})
            rows = result.mappings().fetchall()

            new_buy_ingred_list = []
            for row in rows:
                new_buy_ingred = BuyIngred(
                    user_id=row["user_id"],
                    ingred_nm=row["ingred_nm"],
                    qty=row["qty"],
                    unit_cd=row["unit_cd"],
                    sales_area_type=row["sales_area_type"],
                    sales_area_seq=row["sales_area_seq"],
                    manual_add_flg="F",
                    bought_flg="F"
                )
                new_buy_ingred_list.append(new_buy_ingred)

            self.db.add_all(new_buy_ingred_list)
            self.db.commit()

            return new_buy_ingred_list

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_buy_ingred(self, buy_ingred_id: int, ingred_nm: str, qty: float, unit_cd: str, const_sales_area_type: AppConst):

        try:
            edit_buy_ingred = self.db.query(BuyIngred).filter(BuyIngred.buy_ingred_id == buy_ingred_id).one()
            edit_buy_ingred.ingred_nm = ingred_nm
            edit_buy_ingred.qty = qty
            edit_buy_ingred.unit_cd = unit_cd
            edit_buy_ingred.sales_area_type = const_sales_area_type.val
            edit_buy_ingred.sales_area_seq = const_sales_area_type.sort_seq

            self.db.commit()

            return edit_buy_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_buy_ingred_bought_flg(self, buy_ingred_id: int, bought_flg: str) -> BuyIngred:

        try:
            edit_buy_ingred = self.db.query(BuyIngred).filter(BuyIngred.buy_ingred_id == buy_ingred_id).one_or_none()
            
            # workテーブルなので証跡項目は更新不要
            if edit_buy_ingred:
                edit_buy_ingred.bought_flg = bought_flg
                self.db.commit()
            
            return edit_buy_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_buy_ingred(self, buy_ingred_id: int):

        try:
            self.db.query(BuyIngred).filter(BuyIngred.buy_ingred_id == buy_ingred_id, BuyIngred.user_id == self.user_id).delete()
            self.db.commit()

            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_buy_ingred_all(self):

        try:
            self.db.query(BuyIngred).filter(BuyIngred.user_id == self.user_id).delete()
            self.db.commit()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def reduce_buy_ingred_from_recipe(self, recipe: Recipe):

        try:
            for recipe_ingred in recipe.rel_t_recipe_ingred:

                buy_ingred = self.get_buy_ingred_without_manual_add(recipe_ingred.rel_m_ingred.ingred_nm)
                recalc_qty = self.get_recalc_qty(recipe_ingred)
                reduced_qty = buy_ingred.qty - recalc_qty

                # 減算後、必要量が 0 未満となる場合はレコードを削除
                if reduced_qty <= 0:
                    self.db \
                        .query(BuyIngred) \
                        .filter(
                            BuyIngred.ingred_nm == recipe_ingred.rel_m_ingred.ingred_nm,
                            BuyIngred.user_id == self.user_id,
                            BuyIngred.manual_add_flg == "F",
                        ) \
                        .delete()

                # 減算後、必要量が 0 未満とならない場合は減算後の値で更新
                else:
                    buy_ingred.qty = reduced_qty

            self.db.commit()

            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_recalc_qty(self, recipe_ingred: RecipeIngred) -> float:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred_unit_conv = ingred_crud.get_ingred_unit_conv(recipe_ingred.ingred_id, recipe_ingred.unit_cd)
            recalc_qty = recipe_ingred.qty / ingred_unit_conv.conv_rate

            return recalc_qty

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
