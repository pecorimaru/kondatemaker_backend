from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud import IngredCrud, AppConstCrud
from app.models.display import DefaultSets
from app.utils import constants as const

from app.services.app_const_service import AppConstService

class IngredFormService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def fetch_default_sets_by_ingred(self, ingred_nm: str) -> DefaultSets:

        try:        
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)
            if ingred:
                default_sets = DefaultSets.from_ingred(ingred)
                return default_sets
            return None

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_unit_dict_by_ingred(self, ingred_nm: str) -> dict[str, str]:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred = ingred_crud.get_ingred_from_nm(ingred_nm)

            if ingred:
                # 食材ごとに登録した単位変換情報を単位でリスト化
                unit_cd_list = [ingred_unit_conv.from_unit_cd for ingred_unit_conv in ingred.rel_m_ingred_unit_conv] 

                const_crud = AppConstCrud(self.db)
                const_unit_cd_list = const_crud.get_app_consts(const.APP_CONST_C0002_UNIT_TYPE)

                # 単位変換情報がある場合のみ、選択肢として追加
                unit_dict_by_ingred = {}
                for const_unit_cd in const_unit_cd_list:
                    if const_unit_cd.val in unit_cd_list:
                        unit_dict_by_ingred[const_unit_cd.val] = const_unit_cd.val_content

                return unit_dict_by_ingred

            # 食材マスタに登録がない場合、全ての選択肢を追加
            app_service = AppConstService(self.user_id, self.db)
            unit_dict_by_ingred = app_service.fetch_app_const_dict(const.APP_CONST_C0002_UNIT_TYPE)

            return unit_dict_by_ingred

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_ingred_nm_suggestions(self, input_value: str) -> list[str]:

        try:
            ingred_crud = IngredCrud(self.user_id, self.db)
            ingred_nm_suggestions = ingred_crud.get_ingred_nm_suggestions(input_value)
            return ingred_nm_suggestions

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
