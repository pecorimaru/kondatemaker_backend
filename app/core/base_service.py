from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import inspect

from app.core.method_info import Param
from app.utils.log_utils import logger
from app.utils import message_utils as msg


class BaseService():

    def __init__(self, user_id: int, group_id: int, owner_user_id: int, db: Session):
        self.user_id = user_id
        self.group_id = group_id
        self.owner_user_id = owner_user_id
        self.db = db


    def get_method_nm(self) -> str:
        caller_frame = inspect.stack()[1] 
        method_nm = caller_frame.function
        return method_nm     


    def get_params(self, method_nm: str) -> list[Param]:

        frame = inspect.currentframe().f_back                    # 呼び出し元のフレームを取得
        local_vars = frame.f_locals                              # ローカル変数を取得
        signature = inspect.signature(getattr(self, method_nm))
        params = []
        for param_nm in signature.parameters:
            if param_nm != 'self':
                params.append(Param(param_nm = param_nm, value = str(local_vars.get(param_nm))))
        return params


    def handle_system_error(self, e: Exception, method_nm: str, params: list[Param]):

        if type(e) == HTTPException:
            raise e

        logger.error(msg.get_error_log_message(e, method_nm, params, msg.ME0002_SYSTEM_ERROR))
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = msg.get_message(msg.ME0002_SYSTEM_ERROR)
        )
