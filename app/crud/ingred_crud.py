from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.base_service import BaseService
from app.models import Ingred, IngredUnitConv

from app.utils import db_utils


class IngredCrud(BaseService):
    def __init__(self, user_id: int, db: Session):
        super().__init__(user_id, db)


    def get_ingred(self, ingred_id: int):

        try:
            ingred = self.db.query(Ingred).filter(Ingred.ingred_id == ingred_id, Ingred.owner_user_id == self.user_id).one_or_none()
            return ingred

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_ingred_list(self):

        try:
            ingred_list = self.db.query(Ingred).filter(Ingred.owner_user_id == self.user_id).all()
            return ingred_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_ingred_from_nm(self, ingred_nm: str) -> Ingred:

        try:
            ingred = self.db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == self.user_id).one_or_none()
            return ingred

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_ingred_nm_suggestions(self, input_value: str) -> list[str]:

        try:
            ingred_nm_suggestions = (
                self.db.query(Ingred.ingred_nm) \
                    .filter(
                        or_(
                        Ingred.ingred_nm.like(f"%{input_value}%"),
                        Ingred.ingred_nm_k.like(f"%{input_value}%")
                        ), 
                        Ingred.owner_user_id == self.user_id) \
                    .order_by(Ingred.ingred_nm_k).all()
            )

            # SQLAlchemyでは１項目のみで取得してもタプル型リスト[(Ingred.ingred_nm, ),...]になるため
            # str型リスト[(Ingred.ingred_nm),...]に変換する
            return [name[0] for name in ingred_nm_suggestions] if ingred_nm_suggestions else []

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_ingred(self, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, standard_unit_cd: str, sales_area_type: str) -> Ingred:

            time_stamp = db_utils.get_timestamp()

            try:
                new_ingred = Ingred(
                    ingred_nm = ingred_nm,
                    ingred_nm_k = ingred_nm_k,
                    parent_ingred_nm = parent_ingred_nm,
                    standard_unit_cd = standard_unit_cd,
                    sales_area_type = sales_area_type,
                    owner_user_id = self.user_id,
                    crt_at = time_stamp,
                    upd_at = time_stamp,
                    crt_by = self.user_id,
                    upd_by = self.user_id,
                    version = 0
                )

                self.db.add(new_ingred)
                self.db.commit()
                return new_ingred

            except SQLAlchemyError as e:
                self.db.rollback()
                method_nm = self.get_method_nm()
                self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_ingred(self, ingred_id: int, ingred_nm: str, ingred_nm_k: str, parent_ingred_nm: str, standard_unit_cd: str, sales_area_type: str):

        time_stamp = db_utils.get_timestamp()

        try:
            edit_ingred = self.db.query(Ingred).filter(Ingred.ingred_id == ingred_id, Ingred.owner_user_id == self.user_id).one()
            edit_ingred.ingred_nm = ingred_nm
            edit_ingred.ingred_nm_k = ingred_nm_k
            edit_ingred.parent_ingred_nm = parent_ingred_nm
            edit_ingred.standard_unit_cd = standard_unit_cd
            edit_ingred.sales_area_type = sales_area_type
            edit_ingred.upd_at = time_stamp
            edit_ingred.upd_by = self.user_id
            edit_ingred.version = edit_ingred.version + 1

            self.db.commit()
            return edit_ingred

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred(self, ingred_id: int):

        try:
            self.db.query(Ingred).filter(Ingred.ingred_id == ingred_id, Ingred.owner_user_id == self.user_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_ingred_unit_conv(self, ingred_id: int, from_unit_cd: str) -> IngredUnitConv:

        try:
            ingred_unit_conv = self.db \
                .query(IngredUnitConv) \
                .filter(IngredUnitConv.ingred_id == ingred_id, IngredUnitConv.from_unit_cd == from_unit_cd) \
                .one_or_none();

            return ingred_unit_conv

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def get_ingred_unit_conv_list_without_standard(self, ingred_id: int, standard_unit_cd: str) -> list[IngredUnitConv]:

        try:
            ingred_unit_conv_list = self.db \
                .query(IngredUnitConv) \
                .filter(IngredUnitConv.ingred_id == ingred_id, IngredUnitConv.from_unit_cd != standard_unit_cd) \
                .all();

            return ingred_unit_conv_list

        except SQLAlchemyError as e:
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def create_ingred_unit_conv(self, ingred_id: int, from_unit_cd: str, conv_rate: float) -> IngredUnitConv:

        time_stamp = db_utils.get_timestamp()

        try:
            new_ingred_unit_conv = IngredUnitConv(
                ingred_id = ingred_id,
                from_unit_cd = from_unit_cd,
                conv_rate = conv_rate,
                crt_at = time_stamp,
                upd_at = time_stamp,
                owner_user_id = self.user_id,
                crt_by = self.user_id,
                upd_by = self.user_id,
                version = 0
            )

            self.db.add(new_ingred_unit_conv)
            self.db.commit()
            return new_ingred_unit_conv

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def update_ingred_unit_conv(self, ingred_unit_conv_id: int, ingred_id: int, from_unit_cd: str, conv_rate: float) -> IngredUnitConv:

        time_stamp = db_utils.get_timestamp()

        try:
            edit_ingred_unit_conv = self.db.query(IngredUnitConv).filter(IngredUnitConv.ingred_unit_conv_id == ingred_unit_conv_id).one()
            edit_ingred_unit_conv.ingred_id = ingred_id
            edit_ingred_unit_conv.from_unit_cd = from_unit_cd
            edit_ingred_unit_conv.conv_rate = conv_rate
            edit_ingred_unit_conv.upd_at = time_stamp
            edit_ingred_unit_conv.upd_by = self.user_id
            edit_ingred_unit_conv.version = edit_ingred_unit_conv.version + 1

            self.db.commit()
            return edit_ingred_unit_conv

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred_unit_conv(self, ingred_unit_conv_id: int):

        try:
            self.db.query(IngredUnitConv).filter(IngredUnitConv.ingred_unit_conv_id == ingred_unit_conv_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def delete_ingred_unit_conv_from_ingred(self, ingred_id: int):

        try:
            self.db.query(IngredUnitConv).filter(IngredUnitConv.ingred_id == ingred_id).delete()
            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))


    def replace_ingred_unit_conv(self, ingred_id: int, old_standard_unit_cd: str, new_standard_unit_cd: str):

        time_stamp = db_utils.get_timestamp()

        try:
            old_standard_ingred_unit_conv = self.get_ingred_unit_conv(ingred_id, old_standard_unit_cd)
            new_standard_ingred_unit_conv = self.get_ingred_unit_conv(ingred_id, new_standard_unit_cd)

            # 購入単位(新)が変換単位として登録されている場合
            if new_standard_ingred_unit_conv:
                
                # 購入単位(旧)の変換レートを購入単位(新)で指定していた変換レートで更新
                old_standard_ingred_unit_conv.conv_rate = 1 / new_standard_ingred_unit_conv.conv_rate
                old_standard_ingred_unit_conv.upd_at = time_stamp
                old_standard_ingred_unit_conv.upd_by = self.user_id
                old_standard_ingred_unit_conv.version += 1

                # 購入単位(新)の変換レートは 1.0 固定で更新
                new_standard_ingred_unit_conv.conv_rate = 1
                new_standard_ingred_unit_conv.upd_at = time_stamp
                new_standard_ingred_unit_conv.upd_by = self.user_id
                new_standard_ingred_unit_conv.version += 1

            # 購入単位(新)が変換単位として登録されていない場合
            else:

                # 購入単位(旧)の変換情報は削除
                self.db.query(IngredUnitConv).filter(
                    IngredUnitConv.ingred_id == ingred_id,
                    IngredUnitConv.from_unit_cd == old_standard_unit_cd,
                    IngredUnitConv.owner_user_id == self.user_id,
                ).delete()

                # 購入単位(新)の変換レートは 1.0 固定で新規登録
                self.create_ingred_unit_conv(ingred_id, new_standard_unit_cd, 1)

            self.db.commit()
            return

        except SQLAlchemyError as e:
            self.db.rollback()
            method_nm = self.get_method_nm()
            self.handle_system_error(e, method_nm, self.get_params(method_nm))