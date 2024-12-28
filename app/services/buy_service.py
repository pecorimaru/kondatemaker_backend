from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.models.display import BuyIngredDisp
from app.crud import WorkCrud, AppConstCrud

from app.utils import constants as const


class BuyService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_buy_ingred_list(self) -> list[BuyIngredDisp]:
        
        try: 
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            buy_ingred_list = work_crud.get_buy_ingred_list()
            buy_ingred_list_disp = []
            for buy_ingred in buy_ingred_list:
                buy_ingred_list_disp.append(BuyIngredDisp.from_buy_ingred(buy_ingred))

            return buy_ingred_list_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def switch_completion_state(self, buy_ingred_id: int, bought_flg: str) -> BuyIngredDisp:

        try:
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_buy_ingred = work_crud.update_buy_ingred_bought_flg(buy_ingred_id, bought_flg)
            self.db.commit()

            new_buy_ingred_disp = BuyIngredDisp.from_buy_ingred(new_buy_ingred)
            return new_buy_ingred_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_buy_ingred(self, ingred_nm: str, qty: float, unit_cd: str, sales_area_type: str) -> BuyIngredDisp:

        try:
            const_crud = AppConstCrud(self.db)
            const_sales_area_type = const_crud.get_app_const_from_val(const.APP_CONST_C0004_SALES_AREA_TYPE, sales_area_type)

            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_buy_ingred = work_crud.create_buy_ingred(ingred_nm, qty, unit_cd, const_sales_area_type)
            self.db.commit()

            new_buy_ingred_disp = BuyIngredDisp.from_buy_ingred(new_buy_ingred)
            return new_buy_ingred_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_buy_ingred(self, buy_ingred_id: int, ingred_nm: str, qty: float, unit_cd: str, sales_area_type: str) -> BuyIngredDisp:

        try:
            const_crud = AppConstCrud(self.db)
            const_sales_area_type = const_crud.get_app_const_from_val(const.APP_CONST_C0004_SALES_AREA_TYPE, sales_area_type)

            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            new_buy_ingred = work_crud.update_buy_ingred(buy_ingred_id, ingred_nm, qty, unit_cd, const_sales_area_type)
            self.db.commit()

            new_buy_ingred_disp = BuyIngredDisp.from_buy_ingred(new_buy_ingred)
            return new_buy_ingred_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_buy_ingred(self, buy_ingred_id: int):

        try:
            work_crud = WorkCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            work_crud.delete_buy_ingred(buy_ingred_id)
            self.db.commit()
    
            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
