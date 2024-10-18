from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import src.utils.apiutils as apiutils


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        camel_case_detail = apiutils.convert_dict_to_camel_case({"detail": exc.detail})
        return JSONResponse(
            status_code=exc.status_code,
            content=camel_case_detail
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        camel_case_errors = apiutils.convert_dict_to_camel_case({"detail": exc.errors()})
        return JSONResponse(
            status_code=422,
            content=camel_case_errors
        )