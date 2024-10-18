from sqlalchemy import text
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from pydantic import BaseModel
from datetime import datetime

from src.models.models import Ingred
from src.crud import common as common_crud


def get_ingred(ingred_id: int, user_id, db: Session):

    print(f"ingred_id: {ingred_id}, user_id: {user_id}")
    try:
        ingred = db.query(Ingred).filter(Ingred.ingred_id == ingred_id, Ingred.owner_user_id == user_id).one_or_none()

        if not ingred:
            return None

        return ingred

    except:
        raise

    finally:
        pass