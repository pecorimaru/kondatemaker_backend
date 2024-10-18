from sqlalchemy import text
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from pydantic import BaseModel
from datetime import datetime

from src.models.models import Ingred

from src.models.models import RecipeIngred
from src.models.BuyIngreds import BuyIngreds
from src.crud import common as common_crud

class ToweekRecipe(BaseModel):
    id: int
    name: str


def get_standard_unit_nm(ingred_nm: str, user_id, db: Session):

    try:
        ingred = db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == user_id).one_or_none()

        if not ingred:
            return None

        app_consts = common_crud.get_app_consts("C0002", db)

        for app_const in app_consts:
            if ingred.standard_unit_cd == app_const.val:
                return app_const.val_content

        return None

    except:
        raise

    finally:
        pass


def get_sales_area_nm(ingred_nm: str, user_id, db: Session):

    try:
        ingred = db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == user_id).one_or_none()

        if not ingred:
            return None

        app_consts = common_crud.get_app_consts("C0004", db)

        for app_const in app_consts:
            if ingred.sales_area_type == app_const.val:
                return app_const.val_content

        return None

    except:
        raise

    finally:
        pass



def create_buy_ingreds(ingred_nm: str, qty: float, unit_nm: str, sales_area_nm: str, user_id: str, db: Session):

    try:

        ingred = db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == user_id).one_or_none()

        sales_area = common_crud.get_app_const_from_val("C0004", ingred.sales_area_type, db) if ingred else None

        new_buy_ingreds = BuyIngreds(
            user_id = user_id,
            ingred_nm = ingred_nm,
            qty = qty,
            unit_nm = unit_nm,
            sales_area_nm = sales_area_nm,
            sales_area_seq = sales_area.sort_seq if sales_area else None,
            manual_add_flg = "T",
            bought_flg = "F"
        )

        db.add(new_buy_ingreds)
        db.commit()

        return new_buy_ingreds

    except:
        db.rollback()  # エラー時にロールバック
        raise

    finally:
        pass

