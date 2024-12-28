from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import IngredCrud, RecipeCrud, AppConstCrud 
from app.models.display import IngredDisp, IngredUnitConvDisp
from app.utils import constants as const
from app.validators import ingred_validators

class IngredService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_ingred_list(self):

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            ingred_list = ingred_crud.get_ingred_list()

            const_crud = AppConstCrud(self.db)

            ingred_list_disp = []
            for ingred in ingred_list:    
                ingred_disp = IngredDisp.from_ingred(ingred)
                const_unit = const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred.buy_unit_cd)
                ingred_disp.unit_conv_weight = int(const_unit.generic_item1)
                ingred_list_disp.append(ingred_disp)
            return ingred_list_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_ingred(self, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, buy_unit_cd: str, sales_area_type: str) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            # 食材の一意チェック
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)
            ingred_validators.check_ingred_unique(ingred)

            new_ingred = ingred_crud.create_ingred(ingred_nm, ingred_nm_k, parent_ingred_nm, buy_unit_cd, sales_area_type)
            
            # 購入単位に対する単位変換情報（1 : 1）を登録
            ingred_crud.create_ingred_unit_conv(new_ingred.ingred_id, new_ingred.buy_unit_cd, 1)
            self.db.commit()

            return IngredDisp.from_ingred(new_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_ingred(self, ingred_id: int, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, buy_unit_cd: str, sales_area_type: str) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            old_ingred = ingred_crud.get_ingred(ingred_id)

            # 食材名が変更された場合は食材の一意チェック
            if old_ingred.ingred_nm != ingred_nm:
                ingred = ingred_crud.get_ingred_from_nm(ingred_nm)
                ingred_validators.check_ingred_unique(ingred)

            old_buy_unit_cd = old_ingred.buy_unit_cd
            edit_ingred = ingred_crud.update_ingred(ingred_id, ingred_nm, ingred_nm_k, parent_ingred_nm, buy_unit_cd, sales_area_type)

            # 購入単位が変更された場合は食材単位変換も更新
            if old_buy_unit_cd != edit_ingred.buy_unit_cd:
                ingred_crud.replace_ingred_unit_conv(edit_ingred.ingred_id, old_buy_unit_cd, edit_ingred.buy_unit_cd)

            self.db.commit()

            return IngredDisp.from_ingred(edit_ingred)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred(self, ingred_id: int) -> IngredDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            recipe_ingred = RecipeCrud(self.user_id, self.group_id, self.owner_user_id, self.db)

            # 食材の非参照チェック
            recipe_ingred_list = recipe_ingred.get_recipe_ingred_list_from_ingred(ingred_id)
            ingred_validators.check_ingred_unreferenced(recipe_ingred_list)

            ingred_crud.delete_ingred_unit_convs_from_ingred(ingred_id)
            ingred_crud.delete_ingred(ingred_id)
            self.db.commit()            

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_ingred_unit_conv_list(self, ingred_id: int):

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            ingred = ingred_crud.get_ingred(ingred_id)

            # 購入単位の変換レートは必ず 1.0 となるため除外
            ingred_unit_conv_list = ingred_crud.get_ingred_unit_conv_from_conv_unit_cd_list_without_standard(ingred_id, ingred.buy_unit_cd)
            const_crud = AppConstCrud(self.db)

            ingred_unit_conv_disp_list = []
            for ingred_unit_conv in ingred_unit_conv_list:

                # 取得した単位変換情報に変換ウエイトを付与
                # 例：グラム(g)は1g：nX と表現するとイメージしづらいため、ウエイト込み（100g：nX）で計算する
                ingredUnitConvDisp = IngredUnitConvDisp.from_ingred_unit_conv(ingred_unit_conv)
                const_unit = const_crud.get_app_const_from_val(const.APP_CONST_C0002_UNIT_TYPE, ingred_unit_conv.conv_unit_cd)
                ingredUnitConvDisp.conv_weight = int(const_unit.generic_item1)
                ingred_unit_conv_disp_list.append(ingredUnitConvDisp)

            return ingred_unit_conv_disp_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def add_ingred_unit_conv(self, ingred_id: int, conv_unit_cd: str, conv_rate: float) -> IngredUnitConvDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            app_const_crud = AppConstCrud(self.db)

            # 食材単位変換の一意チェック
            ingred_unit_conv = ingred_crud.get_ingred_unit_conv_from_conv_unit_cd(ingred_id, conv_unit_cd)
            ingred_validators.check_ingred_unit_conv_unique(ingred_unit_conv, app_const_crud)

            new_ingred_unit_conv = ingred_crud.create_ingred_unit_conv(ingred_id, conv_unit_cd, conv_rate)
            self.db.commit()
            
            return IngredUnitConvDisp.from_ingred_unit_conv(new_ingred_unit_conv)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_ingred_unit_conv(self, ingred_unit_conv_id: int, ingred_id: int, conv_unit_cd: str, conv_rate: float) -> IngredUnitConvDisp:

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            app_const_crud = AppConstCrud(self.db)

            # 変換単位が変更された場合は食材単位変換の一意チェック
            old_ingred_unit_conv = ingred_crud.get_ingred_unit_conv(ingred_unit_conv_id)
            if old_ingred_unit_conv.conv_unit_cd != conv_unit_cd:
                ingred_unit_conv = ingred_crud.get_ingred_unit_conv_from_conv_unit_cd(ingred_id, conv_unit_cd)
                ingred_validators.check_ingred_unit_conv_unique(ingred_unit_conv, app_const_crud)

            edit_ingred_unit_conv = ingred_crud.update_ingred_unit_conv(ingred_unit_conv_id, ingred_id, conv_unit_cd, conv_rate)
            self.db.commit()

            return IngredUnitConvDisp.from_ingred_unit_conv(edit_ingred_unit_conv)

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred_unit_conv(self, ingred_unit_conv_id: int):

        try:
            ingred_crud = IngredCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            ingred_crud.delete_ingred_unit_conv(ingred_unit_conv_id)
            self.db.commit()

            return 

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))

