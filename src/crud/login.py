from sqlalchemy import select
from sqlalchemy.orm import Session


from src.models.models import User
from src.models.models import UserConfig
from src.models.models import MenuPlan
from src.models.models import MenuPlanDet
from src.models.models import AppConst


def get_user(mail_addr: str, db: Session) -> User:

    try:
        user = db.query(User).filter(User.mail_addr == mail_addr).one_or_none()
        return user

    finally:
        pass
