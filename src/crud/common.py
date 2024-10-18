from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only

from functools import lru_cache

from src.models.models import AppConst


@lru_cache(maxsize=5000) 
def get_app_const_all(db: Session) -> list[AppConst]:
    try:    
        all_const_list = db.query(AppConst).options(load_only(
            AppConst.type_cd, 
            AppConst.type_nm, 
            AppConst.val, 
            AppConst.val_content,
            AppConst.sort_seq,
            AppConst.generic_item1,
            AppConst.generic_item2
        )).order_by(AppConst.sort_seq).all()
        return all_const_list
    finally:
        pass


def get_app_consts(type_cd: str, db: Session) -> list[AppConst]:

    try:

        all_const_list = get_app_const_all(db)

        const_list = []
        for const in all_const_list:
            if const.type_cd == type_cd:
                const_list.append(const)

        return const_list

    finally:
        pass


def get_app_const_from_val(type_cd: str, val: str, db: Session) -> AppConst:

    try:

        const_list = get_app_consts(type_cd, db)

        for const in const_list:
            if const.val == val:
                return const

        return None

    finally:
        pass


def get_app_const_from_content(type_cd: str, val_content: str, db: Session) -> AppConst:

    try:

        const_list = get_app_consts(type_cd, db)

        for const in const_list:
            if const.val_content == val_content:
                return const

        return None

    finally:
        pass


def get_val(type_cd: str, val_content: str, db: Session):

    app_const = get_app_const_from_content(type_cd, val_content, db)
    return app_const.val if app_const else None


def get_val_content(type_cd: str, val: str, db: Session):

    app_const = get_app_const_from_val(type_cd, val, db)
    return app_const.val_content if app_const else None
