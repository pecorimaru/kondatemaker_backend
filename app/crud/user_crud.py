from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.base_service import BaseService
from app.models import User, UserConfig

from app.utils import db_utils, api_utils, string_utils, constants as const



class UserCrud(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def get_user(self, user_id: int=None) -> User:

        if not user_id:
            user_id = self.user_id

        try:
            user = self.db.query(User).filter(User.user_id == user_id).one_or_none()
            return user

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_user_from_email(self, email_addr: str) -> User:

        try:
            user = self.db.query(User).filter(User.email_addr == email_addr).one_or_none()
            return user

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_user(self, email_addr: str, password: str) -> User:

        try:
            time_stamp = db_utils.get_timestamp()  
            new_user = User(
                user_nm = string_utils.cut_domain(email_addr),
                email_addr = email_addr,
                password = api_utils.get_password_hash(password),
                crt_timestamp = time_stamp,
                crt_user_id = const.ADMIN_USER_ID,
                upd_timestamp = time_stamp,
                upd_user_id = const.ADMIN_USER_ID,
                version = 0
            )
            self.db.add(new_user)
            self.db.flush()

            return new_user

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_user_nm(self, edit_user_nm: str) -> User:

        timestamp = db_utils.get_timestamp()

        try:
            edit_user = self.get_user()
            edit_user.user_nm = edit_user_nm
            edit_user.upd_timestamp = timestamp
            edit_user.upd_user_id = self.user_id
            edit_user.version += 1 

            return 

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_user_password(self, edit_user: User, new_password: str) -> str:

        timestamp = db_utils.get_timestamp()

        try:
            edit_user.password = api_utils.get_password_hash(new_password)
            edit_user.upd_timestamp = timestamp
            edit_user.upd_user_id = edit_user.user_id
            edit_user.version += 1 

            return new_password

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_user_dele_flg(self, dele_flg: str, user_id: int=None) -> User:

        if not user_id:
            user_id = self.user_id

        timestamp = db_utils.get_timestamp()

        try:
            edit_user = self.get_user(user_id)
            edit_user.dele_flg = dele_flg
            edit_user.upd_timestamp = timestamp
            edit_user.upd_user_id = user_id
            edit_user.version += 1 

            return edit_user

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_user(self, user_id: int=None):

        if user_id is None:
            user_id = self.user_id

        try:
            self.db.query(User).filter(User.user_id == self.user_id).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_toweek_menu_plan_id(self) -> str:

        try:
            user_config = self.db.query(UserConfig).filter(
                UserConfig.user_id == self.owner_user_id, 
                UserConfig.config_type == const.USER_CONFIG_TYPE_2_TOWEEK_MENU_PLAN,
            ).one_or_none()

            return user_config.val if user_config else None

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_toweek_menu_plan(self, selected_plan_id: int):

        time_stamp = db_utils.get_timestamp()   

        try:         
            user_config = self.db \
                .query(UserConfig) \
                .filter(UserConfig.user_id == self.user_id, UserConfig.config_type == const.USER_CONFIG_TYPE_2_TOWEEK_MENU_PLAN) \
                .one_or_none()

            if user_config:
                user_config.val = selected_plan_id
                user_config.upd_timestamp = time_stamp
                user_config.upd_user_id = self.user_id
                user_config.version += 1

            # 初回選択時は新規登録
            else:
                new_user_config = UserConfig(
                    user_id = self.user_id,
                    config_type = const.USER_CONFIG_2_TOWEEK_MENU_PLAN,
                    config_val = selected_plan_id,
                    crt_timestamp = time_stamp,
                    crt_user_id = self.user_id,
                    upd_timestamp = time_stamp,
                    upd_user_id = self.user_id,
                    version = 0
                )
                self.db.add(new_user_config)

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_user_config(self, user_id: int, config_type: str) -> UserConfig:

        try:
            user_config = self.db.query(UserConfig).filter(UserConfig.user_id == user_id, UserConfig.config_type == config_type).one_or_none()
            
            return user_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_user_config_from_token(self, token: str) -> UserConfig:

        try:
            user_config = self.db.query(UserConfig).filter(UserConfig.config_type == const.USER_CONFIG_TYPE_5_ACTIVATION_TOKEN, UserConfig.val == token).one_or_none()
            
            return user_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_user_config(self, user_id: int, config_type: str, val: str) -> UserConfig:

        try:
            time_stamp = db_utils.get_timestamp()  
            new_user_config = UserConfig(
                user_id = user_id,
                config_type = config_type,
                val = val,
                crt_timestamp = time_stamp,
                crt_user_id = user_id,
                upd_timestamp = time_stamp,
                upd_user_id = user_id,
                version = 0
            )
            self.db.add(new_user_config)

            return new_user_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_user_config(self, user_id: int, config_type: str, val: str) -> UserConfig:

        timestamp = db_utils.get_timestamp()

        try:    
            edit_user_config = self.get_user_config(user_id, config_type)
            if edit_user_config:
                edit_user_config.val = val
                edit_user_config.upd_timestamp = timestamp
                edit_user_config.upd_user_id = user_id
                edit_user_config.version += 1 

                return edit_user_config
            
            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_user_config(self, user_id: int, config_type: str):

        try:
            self.db.query(UserConfig).filter(UserConfig.user_id == user_id, UserConfig.config_type == config_type).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_user_config_all(self, user_id: int):

        try:
            self.db.query(UserConfig).filter(UserConfig.user_id == user_id).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
            