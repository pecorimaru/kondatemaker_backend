from sqlalchemy.orm import Session, load_only
from sqlalchemy.exc import SQLAlchemyError

from functools import lru_cache

from app.core.base_service import BaseService
from app.models.AppConst import AppConst


class AppConstCrud(BaseService):
    def __init__(self, db: Session):
        super().__init__(None, db)


    @lru_cache(maxsize=5000) 
    def get_app_const_all(self) -> list[AppConst]:

        try:    
            all_const_list = self.db.query(AppConst).options(load_only(
                AppConst.type_cd, 
                AppConst.type_nm, 
                AppConst.val, 
                AppConst.val_content,
                AppConst.sort_seq,
                AppConst.generic_item1,
                AppConst.generic_item2
            )).order_by(AppConst.sort_seq).all()
            return all_const_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_app_consts(self, type_cd: str) -> list[AppConst]:

        all_const_list = self.get_app_const_all()
        const_list = []
        for const in all_const_list:
            if const.type_cd == type_cd:
                const_list.append(const)

        return const_list


    def get_app_const_from_val(self, type_cd: str, val: str) -> AppConst:

        const_list = self.get_app_consts(type_cd)
        for const in const_list:
            if const.val == val:
                return const

        return None


    def get_app_const_from_content(self, type_cd: str, val_content: str) -> AppConst:

        const_list = self.get_app_consts(type_cd)
        for const in const_list:
            if const.val_content == val_content:
                return const

        return None

        