from sqlalchemy import text
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from datetime import datetime

from src.utils.apiutils import CamelModel
from src.models.models import UserConfig
from src.models.models import MenuPlan
from src.models.ToweekRecipes import ToweekRecipes
from src.models.BuyIngreds import BuyIngreds


class ToweekRecipe(CamelModel):
    id: int
    name: str

def get_toweek_menu_plan(user_id: int, db: Session) -> MenuPlan:

    try:

        user_config = db.query(UserConfig).filter(UserConfig.user_id == int(user_id), UserConfig.config_type == "2").one_or_none()

        if user_config:
            menu_plan = db.query(MenuPlan).filter(MenuPlan.menu_plan_id == user_config.config_val).one()
        else:
            menu_plan = None

        return menu_plan

    finally:
        pass


def get_menu_plan_list(user_id: str, db: Session):

    try:

        menu_plan_list = db.execute(select(MenuPlan.menu_plan_nm).filter(MenuPlan.owner_user_id == user_id)).scalars().all()

        if menu_plan_list:
            return menu_plan_list
        return []

    finally:
        pass

def get_toweek_recipes(selected_plan: str, user_id: int, db: Session) -> dict[ToweekRecipe]:

    try:

        menu_plan = db.query(MenuPlan).filter(MenuPlan.menu_plan_nm == selected_plan, MenuPlan.owner_user_id == user_id).one_or_none()

        toweek_recipes = {}
        if not menu_plan:
            return toweek_recipes

        # 日～土のレシピ名を辞書形式でセット（レシピが未登録の曜日も空白でセット）
        for menu_plan_det in menu_plan.rel_t_menu_plan_det:
            toweek_recipes[menu_plan_det.week_day_cd] = ToweekRecipe(
                id=menu_plan_det.recipe_id,
                name=menu_plan_det.rel_t_recipe.recipe_nm
            )

        return toweek_recipes            

    except Exception as e:
        raise

    finally:
        pass



def delete_toweek_recipes(user_id: int, db: Session):

    try:
        stmt = delete(ToweekRecipes).where(ToweekRecipes.user_id == user_id)

        db.execute(stmt)
        db.commit()
        print(f"w_toweek_recipes for userid {user_id} have been deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise


def delete_buy_ingreds(user_id: int, db: Session):

    try:
        stmt = delete(BuyIngreds).where(BuyIngreds.user_id == user_id)

        db.execute(stmt)
        db.commit()
        print(f"w_buy_ingreds for userid {user_id} have been deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise

def update_toweek_plan(selected_plan: str, user_id: int, db: Session):

    try:
        menu_plan = db.query(MenuPlan).filter(MenuPlan.menu_plan_nm == selected_plan, MenuPlan.owner_user_id == user_id).one()

        user_config = db.query(UserConfig).filter(UserConfig.user_id == int(user_id), UserConfig.config_type == "2").one_or_none()

        if user_config:
            user_config.config_val = menu_plan.menu_plan_id
            db.commit()
        
        else:
            time_stamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

            new_user_config = UserConfig(
                user_id = user_id,
                config_type = "2",
                config_val = menu_plan.menu_plan_id,
                crt_at = time_stamp,
                upd_at = time_stamp,
                crt_by = user_id,
                upd_by = user_id,
                version = 0
            )

            db.add(new_user_config)
        
        return

    except Exception as e:
        # エラーが発生した場合はロールバック
        db.rollback()
        print(f'Error occurred: {e}')

    finally:
        pass



def create_toweek_recipes(selected_plan: str, user_id: int, db: Session):

    today = datetime.now().strftime('%Y/%m/%d')

    try:

        toweek_recipes = get_toweek_recipes(selected_plan, user_id, db)

        new_toweek_recipes_list = []
        for weekday_cd in toweek_recipes.keys():
            new_toweek_recipes_list.append(ToweekRecipes(
                user_id = user_id,
                weekday_cd = weekday_cd,
                recipe_id = toweek_recipes[weekday_cd].id,
                crt_dt = today
            ))

        db.add_all(new_toweek_recipes_list)

        db.commit()  # まとめてコミット
    except:
        db.rollback()  # エラー時にロールバック
        raise

    return new_toweek_recipes_list  # 登録された全ユーザーオブジェクトを返す


def create_buy_ingreds(user_id: int, db: Session):

    # # 今週の献立からレシピIDをリスト形式で取得
    # recipe_id_list = [toweek_recipe["id"] for toweek_recipe in toweek_recipes.values()]

    # stmt = select(RecipeIngred).where(RecipeIngred.some_column.in_(recipe_id_list))

    # recipe_ingred_list: list[RecipeIngred] = db.execute(stmt).scalars().all()

    try:

        sql = text(
            """
            SELECT
                  :user_id                     AS user_id
                , t3.ingred_nm                 AS ingred_nm
                , SUM(t2.qty * t4.conv_rate)   AS qty
                , c0002.val_content            AS unit_nm
                , c0004.val_content            AS sales_area_nm
                , c0004.sort_seq               AS sales_area_seq
            FROM
                w_toweek_recipes t1 
                LEFT JOIN t_recipe_ingred t2 
                    ON t1.recipe_id = t2.recipe_id 
                LEFT JOIN m_ingred t3 
                    ON t2.ingred_id = t3.ingred_id 
                LEFT JOIN m_ingred_unit_conv t4 
                    ON t4.ingred_id = t2.ingred_id 
                    AND t4.from_unit_cd = t2.unit_cd 
                LEFT JOIN c_app_const c0002
                    ON c0002.type_cd = 'C0002'
                    AND   c0002.val = t3.standard_unit_cd
                LEFT JOIN c_app_const c0004
                    ON c0004.type_cd = 'C0004'
                    AND c0004.val = t3.sales_area_type
            WHERE
                t1.user_id = :user_id
                AND t2.recipe_ingred_id IS NOT NULL 
            GROUP BY
                t3.ingred_nm
            ORDER BY c0004.sort_seq
            """
        )

        result = db.execute(sql, {"user_id": user_id})
        rows = result.mappings().fetchall()

        new_buy_ingreds_list = []
        for row in rows:
            new_buy_ingreds = BuyIngreds(
                user_id=row["user_id"],
                ingred_nm=row["ingred_nm"],
                qty=row["qty"],
                unit_nm=row["unit_nm"],
                sales_area_nm=row["sales_area_nm"],
                sales_area_seq=row["sales_area_seq"],
                manual_add_flg="F",
                bought_flg="F"
            )
            new_buy_ingreds_list.append(new_buy_ingreds)


        db.add_all(new_buy_ingreds_list)
        db.commit()  # まとめてコミット

    except:
        db.rollback()  # エラー時にロールバック
        raise

    return new_buy_ingreds_list  # 登録された全ユーザーオブジェクトを返す


