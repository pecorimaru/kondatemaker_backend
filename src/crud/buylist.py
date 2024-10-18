from sqlalchemy import text
from sqlalchemy import select, delete
from sqlalchemy.orm import Session


from src.models.models import User
from src.models.models import UserConfig
from src.models.models import RecipeIngred
from src.models.models import MenuPlan
from src.models.models import MenuPlanDet
from src.models.models import AppConst
from src.models.ToweekRecipes import ToweekRecipes
from src.models.BuyIngreds import BuyIngreds


def get_buy_ingreds_list(user_id: int, db: Session) -> list[BuyIngreds]:

    try:

        buy_ingreds_list = db.query(BuyIngreds).filter(BuyIngreds.user_id == user_id).all()
        return buy_ingreds_list           

    finally:
        pass


def update_buy_ingreds_bought_flg(buy_ingreds_id: int, flg: str, db: Session):

    try:

        buy_ingred = db.query(BuyIngreds).filter(BuyIngreds.buy_ingreds_id == buy_ingreds_id).one_or_none()
        
        if buy_ingred:

            buy_ingred.bought_flg = flg
            db.commit()
        
        return f"{buy_ingred} Switched {flg}"

    except Exception as e:
        # エラーが発生した場合はロールバック
        db.rollback()
        print(f'Error occurred: {e}')

    finally:
        pass
