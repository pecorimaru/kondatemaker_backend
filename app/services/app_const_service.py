
from sqlalchemy.orm import Session

from app.core.base_service import BaseService
from app.crud.app_const_crud import AppConstCrud


class AppConstService(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def fetch_app_const_dict(self, type_cd: str):
        
        try: 
            const_crud = AppConstCrud(self.db)
            app_consts = const_crud.get_app_consts(type_cd)
            app_const_dict = {}
            for app_const in app_consts:
                app_const_dict[app_const.val] = app_const.val_content

            return app_const_dict

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
