from fastapi import HTTPException, status

from app.models import Ingred
from app.crud import RecipeCrud
from app.utils import api_utils, constants as const, message_utils as msg


def exist_ingred(ingred: Ingred, ingred_nm: str):
    if not ingred:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = msg.get_message(msg.ME0015_NOT_REGISTABLE_FOREIGN_KEY, "食材", ingred_nm),
        )
