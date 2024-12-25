from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from pydantic import BaseModel
from typing import Optional

import uuid
import contextvars

import app.utils.api_utils as apiutils
from app.utils import message_utils

from app.utils.log_utils import logger


request_id_context = contextvars.ContextVar("request_id", default=None)
url_context = contextvars.ContextVar("url", default=None)
param_context = contextvars.ContextVar("param", default=None)
user_id_context = contextvars.ContextVar("user_id", default=None)
ip_context = contextvars.ContextVar("ip", default=None)


class RequestContextManager:
    def __init__(self):
        self.request_id = request_id_context
        self.url = url_context
        self.param = param_context
        self.user_id = user_id_context
        self.ip = ip_context


    def set_context(self, request_id: str, url: str, ip: str, user_id: Optional[str] = None, param: Optional[str] = None):
        self.request_id.set(request_id)
        self.user_id.set(user_id)
        self.url.set(url)
        self.param.set(param)
        self.ip.set(ip)


class RequestLog(BaseModel):
    request_id: Optional[str]
    user_id: Optional[int]
    url: Optional[str]
    param: Optional[str]
    ip: Optional[str]


context_manager = RequestContextManager()

def global_event_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc):
        camel_case_detail = apiutils.convert_dict_to_camel_case({"detail": exc.detail})
        return JSONResponse(
            status_code=exc.status_code,
            content=camel_case_detail
        )


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        camel_case_errors = apiutils.convert_dict_to_camel_case({"detail": exc.errors()})
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=camel_case_errors
        )
    

    # @app.exception_handler(SQLAlchemyError)
    # async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    #     logger.error(message_utils.get_error_message(exc, request, "ME0002"))
    #     raise HTTPException(
    #         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail = message_utils.get_message("ME0002"),
    #     )


    @app.middleware("http")
    async def log_requests(request: Request, call_next):

        # リクエストIDを取得
        request.state.request_id = str(uuid.uuid4())

        context_manager.set_context(
            request_id = request.state.request_id,
            url = str(request.url.path),
            param = str(request.url.query),
            user_id = request.user_id if hasattr(request, 'user_id') else None,
            ip = request.client.host
        )

        # リクエストログ
        logger.info(f"{request.state.request_id},Request,{request.method},{request.url.path}/{request.url.query}")

        # レスポンスログ
        response = await call_next(request)
        response_log_content = f"{request.state.request_id},Response,Status:{response.status_code},{request.url.path}/{request.url.query}"
        if response.status_code >= 500:
            logger.error(response_log_content)
        elif response.status_code >= 400:
            logger.warn(response_log_content)
        else:
            logger.info(response_log_content)

        return response