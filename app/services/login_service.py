from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

import os
from datetime import datetime, timedelta
from jose import JWTError
from passlib.context import CryptContext

from app.core.base_service import BaseService
from app.models import User, UserConfig, Group
from app.crud import UserCrud, GroupCrud, IngredCrud
from app.validators import user_validators
from app.utils import api_utils, mail_utils, message_utils as msg, constants as const
from app.utils.api_utils import TokenData  

# ハッシュ化用
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def login(self, email: str, password: str) -> TokenData:

        try:
            user_crud = UserCrud(None, None, None, self.db)

            # ユーザー情報の取得
            user = user_crud.get_user_from_email(email)      
            user_validators.verify_password(user, password)
            user_validators.ensure_not_deleted(user)

            # ユーザーがアクティブであることを確認
            user_config = user_crud.get_user_config(user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG)
            user_validators.ensure_activate(user_config)

            current_group = self.get_current_group(user.user_id)
            token_data = api_utils.get_token_data(user.user_id, current_group.group_id, current_group.owner_user_id)

            return token_data

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def google_login(self, email: str) -> TokenData:

        try:

            isActiveAccount = False

            # 既存登録チェック
            user_crud = UserCrud(None, None, None, self.db)
            user = user_crud.get_user_from_email(email)
            if user:

                # アカウントが有効な場合
                if not user.dele_flg == "T":

                    isActiveAccount = True
                    
                    # 新規登録済でアクティベート待ちの場合
                    user_config = user_crud.get_user_config(user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG)
                    if user_config.val == "F":
                        user_crud.update_user_config(user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG, "T")
                        user_crud.delete_user_config(user.user_id, const.USER_CONFIG_TYPE_5_ACTIVATION_TOKEN)
                        self.db.commit()

                else:
                    new_user = user_crud.update_user_dele_flg("F", user.user_id)            
            else:
                new_user = user_crud.create_user(email, "")

            if not isActiveAccount:

                # # グループ登録
                group = self.create_default_group_and_set_current(new_user)

                # React StrictMode による重複エラーが発生した場合は処理を正常終了
                if not group:
                    return

                # ユーザー設定登録・更新・削除
                self.user_config_initialize(new_user.user_id, group.group_id)
                user_crud.create_user_config(new_user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG, "T")

                # adminユーザーが所有している食材を登録
                self.create_default_ingred(new_user.user_id)

                self.db.commit()

            user_id = user.user_id if user else new_user.user_id
            current_group = self.get_current_group(user_id)
            token_data = api_utils.get_token_data(user_id, current_group.group_id, current_group.owner_user_id)

            return token_data

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def refresh_access_token(self, refresh_token: str) -> str:

        try:
            login_info = api_utils.decode_token(refresh_token)

            user_crud = UserCrud(login_info.user_id, login_info.group_id, login_info.owner_user_id, self.db)
            user = user_crud.get_user()
            user_validators.ensure_alive_token(user)
            
            # 新しいアクセストークンを発行
            new_access_token = api_utils.create_access_token(data={
                "user_id": login_info.user_id, 
                "group_id": login_info.group_id, 
                "owner_user_id": login_info.owner_user_id
            })
            
            return new_access_token
            
        except JWTError:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED, 
                detail = msg.get_message(msg.ME0003_SESSION_TIME_OUT),
            )

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
            

    def reset_password(self, email: str):

        try:
            user_crud = UserCrud(None, None, None, self.db)
            user = user_crud.get_user_from_email(email)
            user_validators.exist_account(user)
            user_validators.ensure_not_deleted(user)

            # アクティベーションの確認
            user_config = user_crud.get_user_config(user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG)
            user_validators.ensure_activate(user_config)

            new_password = api_utils.generate_temporary_password()
            user_crud.update_user_password(user, new_password)

            # 仮パスワードをメール送信
            try:
                mail_utils.send_email(
                    to_email=user.email_addr,
                    subject="パスワード再発行のお知らせ",
                    body=f"仮パスワード: {new_password}\nログイン後、パスワードを変更してください。"
                )

            except Exception:
                raise HTTPException(status_code=422, detail=msg.ME0006_MISSING_SEND_MAIL)

            self.db.commit()

            return

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_user(self, email: str, password: str):

        try:
            user_crud = UserCrud(None, None, None, self.db)

            # 既存登録チェック
            user = user_crud.get_user_from_email(email)
            if user:
                # 削除済チェック（有効なアカウントが存在する場合はエラー）
                user_validators.ensure_deleted(user)
                user_crud.user_id = user.user_id
                new_user = user_crud.update_user_password(user, password)
                new_user = user_crud.update_user_dele_flg("F")
            else:
                new_user = user_crud.create_user(email, password)

            token = api_utils.generate_activation_token()

            # ユーザー設定登録
            user_crud.create_user_config(new_user.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG, "F")
            user_crud.create_user_config(new_user.user_id, const.USER_CONFIG_TYPE_5_ACTIVATION_TOKEN, token)

            self.db.commit()

            # アクティベーションリンクを生成
            activation_link = f"{os.getenv("CLIENT_URL")}/activate?token={token}"

            html_content = f"""
                <html>
                <body>
                    <p>以下のリンクをクリックしてアカウントを有効化してください:</p>
                    <p>
                    <a href="{activation_link}">{activation_link}</a>
                    </p>
                </body>
                </html>
            """

            mail_utils.send_email_html(
                to_email = new_user.email_addr,
                subject = "アカウント発行リンク",
                html_content = html_content
            )

            return 

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def activate_user(self, token: str):

        try:
            # ユーザー登録
            user_crud = UserCrud(None, None, None, self.db)
            user_config = user_crud.get_user_config_from_token(token)          

            self.validate_user_config_from_token(user_crud, user_config)

            user = user_crud.get_user(user_config.user_id)

            # グループ登録
            group = self.create_default_group_and_set_current(user)

            # React StrictMode による重複エラーが発生した場合は処理を正常終了
            if not group:
                return

            # ユーザー設定登録・更新・削除
            self.user_config_initialize(user.user_id, group.group_id)

            # adminユーザーが所有している食材を登録
            self.create_default_ingred(user.user_id)

            self.db.commit()

            return

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_current_group(self, user_id: int):

        try:
            user_crud = UserCrud(None, None, None, self.db)
            user_config = user_crud.get_user_config(user_id, const.USER_CONFIG_TYPE_3_CURRENT_GROUP)

            group_crud = GroupCrud(None, None, None, self.db)
            group = group_crud.get_group(int(user_config.val))

            return group

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_default_group_and_set_current(self, user: User) -> Group:

        # グループ登録
        group_crud = GroupCrud(user.user_id, None, user.user_id, self.db)
        default_group_nm = f"{user.user_nm}のグループ"
        group = group_crud.create_group(default_group_nm) 
        
        # React StrictMode による重複エラーが発生した場合は処理を正常終了
        if not group:
            return

        # グループ設定（1:参加フラグ）登録
        group_crud.create_group_config(group.group_id, user.user_id, const.GROUP_CONFIG_TYPE_1_JOIN_FLG, "T")

        return group


    def user_config_initialize(self, user_id: int, group_id: int):
    
        # ユーザー設定登録・更新・削除
        user_crud = UserCrud(user_id, group_id, user_id, self.db)
        user_crud.create_user_config(user_id, const.USER_CONFIG_TYPE_1_START_WEEKDAY, "2")
        user_crud.create_user_config(user_id, const.USER_CONFIG_TYPE_3_CURRENT_GROUP, str(group_id))
        user_crud.update_user_config(user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG, "T")
        user_crud.delete_user_config(user_id, const.USER_CONFIG_TYPE_5_ACTIVATION_TOKEN)

        return


    def create_default_ingred(self, user_id: int):

        # adminユーザーが所有している食材を登録
        fetch_ingred_crud = IngredCrud(user_id, None, const.ADMIN_USER_ID, self.db)
        default_ingred_list = fetch_ingred_crud.get_ingred_list()

        rgtr_ingred_crud = IngredCrud(user_id, None, user_id, self.db)

        for default_ingred in default_ingred_list:

            new_ingred = rgtr_ingred_crud.create_ingred(
                ingred_nm = default_ingred.ingred_nm,
                ingred_nm_k = default_ingred.ingred_nm_k,
                parent_ingred_nm = default_ingred.parent_ingred_nm,
                buy_unit_cd = default_ingred.buy_unit_cd,
                sales_area_type = default_ingred.sales_area_type,
            )

            for default_ingred_unit_conv in default_ingred.rel_m_ingred_unit_conv:
                rgtr_ingred_crud.create_ingred_unit_conv(
                    ingred_id = new_ingred.ingred_id,
                    conv_unit_cd = default_ingred_unit_conv.conv_unit_cd,
                    conv_rate = default_ingred_unit_conv.conv_rate
                )


    def validate_user_config_from_token(self, user_crud: UserCrud, user_config: UserConfig):

        # ユーザー設定（アクティベーショントークン）が取得できない場合
        if not user_config:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail = msg.get_message(msg.MW0003_URL_INVALID)
            )

        # アクティベーショントークン発行から30分以上経過した場合
        if (user_config.crt_timestamp + timedelta(seconds=30 * 60)).timestamp() <= datetime.now().timestamp():
       
            user_crud.delete_user_config(user_config.user_id, const.USER_CONFIG_TYPE_4_ACTIVATE_FLG)
            user_crud.delete_user_config(user_config.user_id, const.USER_CONFIG_TYPE_5_ACTIVATION_TOKEN)
            user_crud.delete_user(user_config.user_id)
            self.db.commit()

            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail = msg.get_message(msg.MW0004_URL_EXPIRED)
            )