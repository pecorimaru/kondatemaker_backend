from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import os
from datetime import datetime, timedelta

from app.core.base_service import BaseService
from app.crud import *
from app.models.display import UserDisp, GroupDisp, GroupMemberDisp
from app.models import GroupConfig
from app.utils import api_utils, mail_utils, message_utils as msg, constants as const
from app.utils.api_utils import TokenData

class SettingService(BaseService):
    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        super().__init__(user_id, group_id, owner_user_id, db)


    def fetch_login_user(self) -> str:
    
        try:
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user = user_crud.get_user()

            user_disp = UserDisp(user_nm = user.user_nm)

            return user_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_user_nm(self, edit_user_nm: str):

        try:
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)            
            user_crud.update_user_nm(edit_user_nm)
            
            self.db.commit()

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def change_password(self, current_password: str, new_password: str):

        try:
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user = user_crud.get_user()

            if not api_utils.verify_password(current_password, user.password):
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = msg.get_message(msg.ME0005_PASSWORD_INVALID),
                )
            
            user_crud.update_user_password(user, new_password)
            self.db.commit()

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_user(self):

        try:
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group_list = group_crud.get_group_list_from_owner_user_id(self.user_id)

            for group in group_list:

                # ワークテーブルデータの削除
                work_crud = WorkCrud(self.user_id, group.group_id, group.owner_user_id, self.db)
                work_crud.delete_buy_ingred_all()
                work_crud.delete_toweek_menu_plan_det_all()

                # 献立プランデータの削除
                menu_plan_crud = MenuPlanCrud(self.user_id, group.group_id, group.owner_user_id, self.db)
                menu_plan_list = menu_plan_crud.get_menu_plan_list()
                for menu_plan in menu_plan_list:
                    menu_plan_crud.delete_menu_plan_det_from_menu_plan(menu_plan.menu_plan_id)
                menu_plan_crud.delete_menu_plan_all()

                # レシピデータの削除
                recipe_crud = RecipeCrud(self.user_id, group.group_id, group.owner_user_id, self.db)
                recipe_list = recipe_crud.get_recipe_list()
                for recipe in recipe_list:
                    recipe_crud.delete_recipe_ingreds_from_recipe(recipe.recipe_id)
                recipe_crud.delete_recipes_from_owner()

                # 食材データの削除
                ingred_crud = IngredCrud(self.user_id, group.group_id, group.owner_user_id, self.db)
                ingred_list = ingred_crud.get_ingred_list()
                for ingred in ingred_list:
                    ingred_crud.delete_ingred_unit_convs_from_ingred(ingred.ingred_id)
                ingred_crud.delete_ingred_all()

                group_crud.delete_group_config_all(group.group_id)

            # 招待中のグループがある場合は削除
            group_crud.delete_group_config_all_from_user_id(self.user_id)
            
            # 自身が所有者となるグループを全て削除（想定上は１件のみ）
            group_crud.delete_group_all(self.user_id)

            # ユーザーの削除
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user_crud.delete_user_config_all(self.user_id)
            user_crud.update_user_dele_flg("T")  # 外部キーの紐付きが多いため論理削除

            self.db.commit()

            return

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_current_group(self) -> GroupDisp:
    
        try:
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group = group_crud.get_group(self.group_id)

            if not group:
                return

            group_disp = GroupDisp(
                group_id = group.group_id,
                group_nm = group.group_nm,
                current_flg = "T",
                has_ownership = "T" if group.owner_user_id == self.user_id else "F",
            )

            return group_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_group_list(self) -> list[GroupDisp]:
    
        try:
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group_config_list = group_crud.get_group_config_list_from_join_user()

            group_disp_list = []
            for group_config in group_config_list:
                group_disp_list.append(GroupDisp(
                    group_id = group_config.group_id,
                    group_nm = group_config.rel_m_group.group_nm,
                    current_flg = "T" if group_config.group_id == self.group_id else "F",
                ))

            return group_disp_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def fetch_group_member_list(self) -> list[GroupDisp]:
    
        try:
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group_config_list = group_crud.get_group_config_member_list()

            group_member_list = []
            for group_config in group_config_list:
                group_member_list.append(GroupMemberDisp(
                    user_nm = group_config.rel_m_user.user_nm,
                    owner_flg = "T" if group_config.user_id == group_config.rel_m_group.owner_user_id else "F",
                ))

            return group_member_list

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def edit_group_nm(self, edit_group_nm: str):

        try:
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)            
            edit_group = group_crud.update_group_nm(edit_group_nm)

            self.db.commit()

            edit_group_disp = GroupDisp(
                group_id = edit_group.group_id,
                group_nm = edit_group.group_nm,
                current_flg = "T",
                has_ownership = "T",
            )

            return edit_group_disp

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))

    
    def member_invite(self, to_email: str):

        try:
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)            
            invite_user = user_crud.get_user_from_email(to_email)

            # 招待相手がアカウント登録されていない場合
            if not invite_user:
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail = msg.get_message(msg.ME0007_EMAIL_NOT_SIGNUPED),
                )

            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)  
            group_config = group_crud.get_group_config(self.group_id, invite_user.user_id, const.GROUP_CONFIG_TYPE_1_JOIN_FLG)

            if group_config:
                # 既に参加済の場合
                if group_config.val == "T":
                    raise HTTPException(
                        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail = msg.get_message(msg.ME0008_EMAIL_ALREADY_JOINED),
                    )
                
                # 未参加（招待済）の場合、前回招待時の発行URLを無効化
                group_crud.delete_group_config(self.group_id, invite_user.user_id, const.GROUP_CONFIG_TYPE_5_INVITE_TOKEN)

            else:
                group_crud.create_group_config(self.group_id, invite_user.user_id, const.GROUP_CONFIG_TYPE_1_JOIN_FLG, "F")

            token = api_utils.generate_activation_token()
            group_crud.create_group_config(self.group_id, invite_user.user_id, const.GROUP_CONFIG_TYPE_5_INVITE_TOKEN, token)

            self.db.commit()

            user = user_crud.get_user()

            # グループ参加リンクを生成
            group_join_link = f"{os.getenv("CLIENT_URL")}/joinGroup?token={token}"

            html_content = f"""
                <html>
                <body>
                    <p>{user.user_nm}さんから招待されました。下記のURLをクリックしてグループに参加してください。</p>
                    <a href="{group_join_link}">{group_join_link}</a>
                    <br>
                    <p>※本メールに心当たりがない場合は無視してください。</p>
                </body>
                </html>
            """

            try:
                mail_utils.send_email_html(
                    to_email = to_email,
                    subject = "グループ招待",
                    html_content = html_content
                )

            except Exception:
                raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
                    detail = msg.ME0006_MISSING_SEND_MAIL
                )

            return 

        except Exception as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def join_group(self, token: str):

        try:
            # ユーザー登録
            group_crud = GroupCrud(None, None, None, self.db)
            group_config = group_crud.get_group_config_from_token(token)          

            self.validate_group_config_from_token(group_crud, group_config)

            user_crud = UserCrud(group_config.user_id, group_config.group_id, None, self.db)
            user = user_crud.get_user()
            group_crud.user_id = user.user_id

            group_crud.update_group_config(group_config.group_id, user.user_id, const.GROUP_CONFIG_TYPE_1_JOIN_FLG, "T")
            group_crud.delete_group_config(group_config.group_id, user.user_id, const.GROUP_CONFIG_TYPE_5_INVITE_TOKEN)

            self.db.commit()

            return 

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def validate_group_config_from_token(self, group_crud: GroupCrud, group_config: GroupConfig):

        # グループ設定（グループ招待トークン）が取得できない場合
        if not group_config:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail = msg.get_message(msg.MW0005_INVITE_URL_IVALID)
            )

        # グループ招待トークン発行から30分以上経過した場合
        if (group_config.crt_timestamp + timedelta(seconds=30 * 60)).timestamp() <= datetime.now().timestamp():

            group_crud.delete_group_config(group_config.group_id, group_config.user_id, const.GROUP_CONFIG_TYPE_5_INVITE_TOKEN)
            self.db.commit()

            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail = msg.get_message(msg.MW0006_INVITE_URL_EXPIRED)
            )


    def change_group(self, group_id: int) -> TokenData:

        try:
            # ユーザー設定（現在のグループ）を更新
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user_crud.update_user_config(self.user_id, const.USER_CONFIG_TYPE_3_CURRENT_GROUP, str(group_id))

            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group = group_crud.get_group(group_id)

            self.db.commit()

            token_data = api_utils.get_token_data(self.user_id, group_id, group.owner_user_id)

            return token_data

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def exit_group(self) -> TokenData:

        try:
            # ユーザー登録
            group_crud = GroupCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            group_crud.delete_group_config(self.group_id, self.user_id, const.GROUP_CONFIG_TYPE_1_JOIN_FLG) 

            # 自身が所有者となるグループを取得して現在のグループに指定    
            group_list = group_crud.get_group_list_from_owner_user_id(self.user_id)
            self_group_id = group_list[0].group_id
            user_crud = UserCrud(self.user_id, self.group_id, self.owner_user_id, self.db)
            user_crud.update_user_config(self.user_id, const.USER_CONFIG_TYPE_3_CURRENT_GROUP, str(self_group_id))

            self.db.commit()

            token_data = api_utils.get_token_data(self.user_id, self_group_id, self.user_id)

            return token_data

        except Exception as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))
