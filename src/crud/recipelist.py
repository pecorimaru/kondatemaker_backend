from sqlalchemy import text
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from pydantic import BaseModel
from datetime import datetime

from src.models.models import RecipeIngred
from src.models.models import Recipe
from src.models.models import Ingred
from src.crud import common as common_crud


def get_recipe_list(user_id: int, db: Session) -> list[Recipe]:

    try:

        recipe_list_query = db.query(
            Recipe.recipe_id,
            Recipe.recipe_nm,
            Recipe.recipe_nm_k,
            Recipe.recipe_type,
            Recipe.recipe_url,
            Recipe.visibility_flg
        )

        recipe_list = recipe_list_query.filter(Recipe.owner_id == user_id).all()



        return recipe_list           

    finally:
        pass

def get_recipe_ingred_list(recipe_id: int, db: Session):

    try:
        sql = text(
            """
            SELECT
                  t1.recipe_id
                , t1.recipe_ingred_id  
                , m1.ingred_nm
                , t1.qty
                , c0002.val_content AS unit_nm
            FROM
                t_recipe_ingred t1 
                LEFT JOIN m_ingred m1 
                    ON t1.ingred_id = m1.ingred_id 
                LEFT JOIN c_app_const c0002 
                    ON c0002.type_cd = 'C0002' 
                    AND c0002.val = t1.unit_cd
            WHERE
                t1.recipe_id = :recipe_id
            ;
            """
        )

        recipe_ingred_list = db.execute(sql, {"recipe_id": recipe_id})

        return recipe_ingred_list

    finally:
        pass

def create_recipe(recipe_nm: str, recipe_nm_kana: str, recipe_type: str, recipe_url: str, user_id: int, db: Session) -> Recipe:

    try:

        time_stamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        new_recipe = Recipe(
            recipe_nm = recipe_nm,
            recipe_nm_k = recipe_nm_kana,
            recipe_type = recipe_type["cd"],
            owner_id = user_id,
            recipe_url = recipe_url,
            visibility_flg = "F",
            crt_at = time_stamp,
            upd_at = time_stamp,
            crt_by = user_id,
            upd_by = user_id,
            version = 0
        )

        db.add(new_recipe)
        db.commit()

        return new_recipe

    except:
        db.rollback()  # エラー時にロールバック
        raise

    finally:
        pass


def create_recipe_ingred(recipe_id: int, ingred_nm: str, qty: float, unit_nm: str, user_id: str, db: Session):

    try:

        ingred = db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == user_id).one_or_none()

        app_const = common_crud.get_app_const_from_content("C0002", unit_nm, db)
        unit_cd = app_const.val if app_const else None

        time_stamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        new_recipe_ingred = RecipeIngred(
            recipe_id = recipe_id,
            ingred_id = ingred.ingred_id,
            qty = qty,
            unit_cd = unit_cd,
            crt_at = time_stamp,
            upd_at = time_stamp,
            crt_by = user_id,
            upd_by = user_id,
            version = 0
        )

        db.add(new_recipe_ingred)
        db.commit()

        return new_recipe_ingred

    except:
        db.rollback()  # エラー時にロールバック
        raise

    finally:
        pass

def update_recipe(recipe_id: int, recipe_nm: str, recipe_nm_kana: str, recipe_type: dict, recipe_url: str, user_id: int, db: Session):

    try:

        edit_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).one()

        time_stamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        edit_recipe.recipe_nm = recipe_nm
        edit_recipe.recipe_nm_k = recipe_nm_kana
        edit_recipe.recipe_type = recipe_type["cd"]
        edit_recipe.recipe_url = recipe_url
        edit_recipe.upd_at = time_stamp
        edit_recipe.upd_by = user_id
        edit_recipe.version = edit_recipe.version + 1

        db.commit()

        return edit_recipe

    except:
        db.rollback()  # エラー時にロールバック
        raise

    finally:
        pass

def delete_recipe(recipe_id: int, user_id: int, db: Session) -> bool:

    try:
        print(f"recipe_id delete: {recipe_id}")
        db.query(Recipe).filter(Recipe.recipe_id == recipe_id, Recipe.owner_id == user_id).delete()
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        pass

def update_recipe_ingred(recipe_ingred_id: int, ingred_nm: str, qty: float, unit_nm: str, user_id: int, db: Session):

    try:

        edit_recipe_ingred = db.query(RecipeIngred).filter(RecipeIngred.recipe_ingred_id == recipe_ingred_id).one()

        ingred = db.query(Ingred).filter(Ingred.ingred_nm == ingred_nm, Ingred.owner_user_id == user_id).one_or_none()

        app_const = common_crud.get_app_const_from_content("C0002", unit_nm, db)
        unit_cd = app_const.val if app_const else None

        time_stamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        edit_recipe_ingred.ingred_id = ingred.ingred_id
        edit_recipe_ingred.qty = qty
        edit_recipe_ingred.unit_cd = unit_cd
        edit_recipe_ingred.upd_at = time_stamp
        edit_recipe_ingred.upd_by = user_id
        edit_recipe_ingred.version = edit_recipe_ingred.version + 1


        db.commit()

        return edit_recipe_ingred

    except:
        db.rollback()  # エラー時にロールバック
        raise

    finally:
        pass


def delete_recipe_ingred(recipe_ingred_id: int, db: Session) -> bool:

    try:
        print(f"recipe_ingred_id delete: {recipe_ingred_id}")
        db.query(RecipeIngred).filter(RecipeIngred.recipe_ingred_id == recipe_ingred_id).delete()
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        pass