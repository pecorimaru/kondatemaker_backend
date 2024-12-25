from pydantic import BaseModel
from typing import Optional

class Param(BaseModel):
    param_nm: str
    value: Optional[str]=None

class MethodInfo(BaseModel):
    method_nm: str
    params: list[Param]