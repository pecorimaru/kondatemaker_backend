from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.base_service import BaseService
from app.utils.api_utils import CamelModel
from app.models import User, UserConfig

from app.utils import db_utils, constants as const


# class UserDisp(CamelModel):
#     user_id: int
#     user_nm: str


class UserCrud(BaseService):

    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def get_user(self, mail_addr: str) -> User:

        try:
            user = self.db.query(User).filter(User.mail_addr == mail_addr).one_or_none()
            return user

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_toweek_menu_plan_id(self) -> str:

        try:
            user_config = self.db.query(UserConfig).filter(UserConfig.user_id == self.user_id, UserConfig.config_type == "2").one_or_none()
            return user_config.config_val if user_config else None

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_toweek_menu_plan(self, selected_plan_id: int):

        try:
            time_stamp = db_utils.get_timestamp()            
            user_config = self.db \
                .query(UserConfig) \
                .filter(UserConfig.user_id == self.user_id, UserConfig.config_type == const.USER_CONFIG_2_TOWEEK_MENU_PLAN) \
                .one_or_none()

            if user_config:
                user_config.config_val = selected_plan_id
                user_config.upd_at = time_stamp
                user_config.upd_by = self.user_id
                self.db.commit()

            # 初回選択時は新規登録
            else:
                new_user_config = UserConfig(
                    user_id = self.user_id,
                    config_type = const.USER_CONFIG_2_TOWEEK_MENU_PLAN,
                    config_val = selected_plan_id,
                    crt_at = time_stamp,
                    upd_at = time_stamp,
                    crt_by = self.user_id,
                    upd_by = self.user_id,
                    version = 0
                )
                self.db.add(new_user_config)

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))