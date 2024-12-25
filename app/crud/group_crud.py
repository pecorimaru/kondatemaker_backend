from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.base_service import BaseService
from app.models import Group, GroupConfig

from app.utils import db_utils, constants as const, message_utils as msg
from app.utils.log_utils import logger

class GroupCrud(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def get_group(self, group_id: int) -> Group:

        try:
            group = self.db.query(Group).filter(Group.group_id == group_id).one_or_none()
            return group

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_from_group_nm(self, group_nm: int) -> Group:

        try:
            group = self.db.query(Group).filter(Group.group_nm == group_nm, Group.owner_user_id == self.owner_user_id).one_or_none()
            return group

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_list_from_owner_user_id(self, owner_user_id: int) -> list[Group]:

        try:
            group_list = self.db.query(Group).filter(Group.owner_user_id == owner_user_id).all()
            return group_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_group(self, group_nm: str) -> Group:

        try:
            time_stamp = db_utils.get_timestamp()  
            new_group = Group(
                group_nm = group_nm,
                owner_user_id = self.user_id,
                crt_timestamp = time_stamp,
                crt_user_id = self.user_id,
                upd_timestamp = time_stamp,
                upd_user_id = self.user_id,
                version = 0
            )
            self.db.add(new_group)
            self.db.flush()

            return new_group

        except IntegrityError as e:
            logger.warn(msg.get_log_message(msg.MW0007_GROUP_RGTR_CONFLICT))
            return None

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_group_nm(self, edit_group_nm: str) -> Group:

        time_stamp = db_utils.get_timestamp()  

        try:
            edit_group = self.get_group(self.group_id)
            edit_group.group_nm = edit_group_nm
            edit_group.upd_timestamp = time_stamp,
            edit_group.upd_user_id = self.user_id,
            edit_group.version += 1

            return edit_group

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_group_all(self, owner_user_id: int):

        try:
            self.db.query(Group).filter(Group.owner_user_id == owner_user_id).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_config(self, group_id: int, user_id: int, config_type: str) -> GroupConfig:

        try:
            group_config = self.db.query(GroupConfig).filter(
                GroupConfig.group_id == group_id,
                GroupConfig.user_id == user_id, 
                GroupConfig.config_type == config_type,
            ).one_or_none()
            
            return group_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_config_from_token(self, token: str) -> GroupConfig:

        try:
            group_config = self.db.query(GroupConfig).filter(
                GroupConfig.config_type == const.GROUP_CONFIG_TYPE_5_INVITE_TOKEN,
                GroupConfig.val == token,
            ).one_or_none()
            
            return group_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_config_list_from_join_user(self) -> list[GroupConfig]:

        try:
            group_config_list = self.db.query(GroupConfig).filter(
                GroupConfig.user_id == self.user_id, 
                GroupConfig.config_type == const.GROUP_CONFIG_TYPE_1_JOIN_FLG,
                GroupConfig.val == "T",
            ).all()
            
            return group_config_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_group_config_member_list(self) -> list[GroupConfig]:

        try:
            group_config_list = self.db.query(GroupConfig).filter(
                GroupConfig.group_id == self.group_id, 
                GroupConfig.config_type == const.GROUP_CONFIG_TYPE_1_JOIN_FLG,
                GroupConfig.val == "T",
            ).all()
            
            return group_config_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_group_config(self, group_id: int, user_id: int, config_type: str, val: str) -> GroupConfig:

        time_stamp = db_utils.get_timestamp()  

        try:
            new_group_config = GroupConfig(
                group_id = group_id,
                user_id = user_id,
                config_type = config_type,
                val = val,
                crt_timestamp = time_stamp,
                crt_user_id = self.user_id,
                upd_timestamp = time_stamp,
                upd_user_id = self.user_id,
                version = 0
            )
            self.db.add(new_group_config)

            return new_group_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_group_config(self, group_id: int, user_id: int, config_type: str, val: str) -> GroupConfig:

        time_stamp = db_utils.get_timestamp()  

        try:
            edit_group_config = self.get_group_config(group_id, user_id, config_type)
            edit_group_config.val = val
            edit_group_config.upd_timestamp = time_stamp
            edit_group_config.upd_user_id = self.user_id
            edit_group_config.version += 1

            return edit_group_config

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_group_config(self, group_id: int, user_id: int, config_type: str):

        if not user_id:
            user_id = self.user_id

        try:
            self.db.query(GroupConfig).filter(
                GroupConfig.group_id == group_id,
                GroupConfig.user_id == user_id,
                GroupConfig.config_type == config_type,
            ).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_group_config_all(self, group_id: int):

        try:
            self.db.query(GroupConfig).filter(GroupConfig.group_id == group_id).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_group_config_all_from_user_id(self, user_id: int):

        try:
            self.db.query(GroupConfig).filter(GroupConfig.user_id == user_id).delete()

            return

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))