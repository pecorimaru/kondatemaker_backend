from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import IngredCrud, AppConstCrud 
from app.models.display import IngredDisp, IngredUnitConvDisp

from app.utils import constants as const


class IngredService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def fetch_ingred_list(self):

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred_list = ingred_crud.get_ingred_list()

            const_crud = AppConstCrud(self.db)

            ingred_list_disp = []
            for ingred in ingred_list:    
                ingred_disp = IngredDisp.from_ingred(ingred)
                const_unit = const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred.standard_unit_cd)
                ingred_disp.unit_conv_weight = int(const_unit.generic_item1)
                ingred_list_disp.append(ingred_disp)
            return ingred_list_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_ingred(self, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, standard_unit_cd: str, sales_area_type: str) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            new_ingred = ingred_crud.create_ingred(ingred_nm, ingred_nm_k, parent_ingred_nm, standard_unit_cd, sales_area_type)
            
            # 購入単位に対する単位変換情報（1 : 1）を登録
            ingred_crud.create_ingred_unit_conv(new_ingred.ingred_id, new_ingred.standard_unit_cd, 1)

            return IngredDisp.from_ingred(new_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_ingred(self, ingred_id: int, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, standard_unit_cd: str, sales_area_type: str) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            old_ingred = ingred_crud.get_ingred(ingred_id)
            old_standard_unit_cd = old_ingred.standard_unit_cd

            edit_ingred = ingred_crud.update_ingred(ingred_id, ingred_nm, ingred_nm_k, parent_ingred_nm, standard_unit_cd, sales_area_type)

            if old_standard_unit_cd != edit_ingred.standard_unit_cd:

                # 食材単位変換を更新
                ingred_crud.replace_ingred_unit_conv(edit_ingred.ingred_id, old_standard_unit_cd, edit_ingred.standard_unit_cd)

            return IngredDisp.from_ingred(edit_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred(self, ingred_id: int) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred_crud.delete_ingred_unit_conv_from_ingred(ingred_id)
            ingred_crud.delete_ingred(ingred_id)

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_ingred_unit_conv_list(self, ingred_id: int):

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred = ingred_crud.get_ingred(ingred_id)

            # 購入単位の変換レートは必ず 1.0 となるため除外
            ingred_unit_conv_list = ingred_crud.get_ingred_unit_conv_list_without_standard(ingred_id, ingred.standard_unit_cd)
            const_crud = AppConstCrud(self.db)

            ingred_unit_conv_disp_list = []
            for ingred_unit_conv in ingred_unit_conv_list:

                # 取得した単位変換情報に変換ウエイトを付与
                ingredUnitConvDisp = IngredUnitConvDisp.from_ingred_unit_conv(ingred_unit_conv)
                const_unit = const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred_unit_conv.from_unit_cd)
                ingredUnitConvDisp.conv_weight = int(const_unit.generic_item1)
                ingred_unit_conv_disp_list.append(ingredUnitConvDisp)

            return ingred_unit_conv_disp_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_ingred_unit_conv(self, ingred_id: int, from_unit_cd: str, conv_rate: float) -> IngredUnitConvDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            new_ingred_unit_conv = ingred_crud.create_ingred_unit_conv(ingred_id, from_unit_cd, conv_rate)
            
            return IngredUnitConvDisp.from_ingred_unit_conv(new_ingred_unit_conv)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_ingred_unit_conv(self, ingred_unit_conv_id: int, ingred_id: int, from_unit_cd: str, conv_rate: float) -> IngredUnitConvDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            new_ingred_unit_conv = ingred_crud.update_ingred_unit_conv(ingred_unit_conv_id, ingred_id, from_unit_cd, conv_rate)

            return IngredUnitConvDisp.from_ingred_unit_conv(new_ingred_unit_conv)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred_unit_conv(self, ingred_unit_conv_id: int):

        try:
            ingred_crud = IngredCrud(None, self.db)
            ingred_crud.delete_ingred_unit_conv(ingred_unit_conv_id)

            return 

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))

