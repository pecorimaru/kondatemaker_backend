from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from typing import Optional

from app.db.session import get_db
from app.utils.api_utils import CamelModel
from app.models.display import IngredDisp, IngredUnitConvDisp

from app.services import IngredService


router = APIRouter()


class SubmitAddIngredRequest(CamelModel):
    ingred_nm: str
    ingred_nm_k: Optional[str]=None
    parent_ingred_nm: str
    standard_unit_cd: str
    sales_area_type: Optional[str]=None
    user_id: int

class SubmitAddIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred: IngredDisp

class SubmitEditIngredRequest(CamelModel):
    ingred_id: int
    ingred_nm: str
    ingred_nm_k: Optional[str]=None
    parent_ingred_nm: str
    standard_unit_cd: str
    sales_area_type: Optional[str]=None
    user_id: int

class SubmitEditIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    edit_ingred: IngredDisp

class SubmitDeleteIngredResponse(CamelModel):
    status_code: int
    message: Optional[str]=None

class SubmitAddIngredUnitConvRequest(CamelModel):
    ingred_id: int
    from_unit_cd: str
    conv_rate: float
    user_id: int

class SubmitAddIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred_unit_conv: IngredUnitConvDisp

class SubmitUpdateIngredUnitConvRequest(CamelModel):
    ingred_unit_conv_id: int
    ingred_id: int
    from_unit_cd: str
    conv_rate: float
    user_id: int

class SubmitUpdateIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None
    new_ingred_unit_conv: IngredUnitConvDisp

class SubmitDeleteIngredUnitConvRequest(CamelModel):
    ingred_unit_conv_id: int

class SubmitDeleteIngredUnitConvResponse(CamelModel):
    status_code: int
    message: Optional[str]=None


@router.get("/ingredList/{query_params}")
def fetch_ingred_list(user_id: int, db: Session = Depends(get_db)):
    
    ingred_service = IngredService(user_id, db)
    ingred_list = ingred_service.fetch_ingred_list()
    return ingred_list


@router.post("/submitAddIngred", response_model=SubmitAddIngredResponse)
async def submit_add_ingred(request: SubmitAddIngredRequest, db: Session = Depends(get_db)):

    ingred_service = IngredService(request.user_id, db)
    new_ingred = ingred_service.add_ingred(request.ingred_nm, request.ingred_nm_k, request.parent_ingred_nm, request.standard_unit_cd, request.sales_area_type)
    return SubmitAddIngredResponse(
        status_code = status.HTTP_200_OK,
        new_ingred = new_ingred,
    )


@router.put("/submitEditIngred", response_model=SubmitEditIngredResponse)
async def submit_edit_ingred(request: SubmitEditIngredRequest, db: Session = Depends(get_db)):

    ingred_service = IngredService(request.user_id, db)
    edit_ingred = ingred_service.edit_ingred(request.ingred_id, request.ingred_nm, request.ingred_nm_k, request.parent_ingred_nm, request.standard_unit_cd, request.sales_area_type)
    return SubmitEditIngredResponse(
        status_code = status.HTTP_200_OK,
        edit_ingred = edit_ingred
    )


@router.delete("/submitDeleteIngred/{query_params}", response_model=SubmitDeleteIngredResponse)
async def submit_delete_ingred(ingred_id: int, user_id: int, db: Session = Depends(get_db)):

    ingred_service = IngredService(user_id, db)
    ingred_service.delete_ingred(ingred_id)
    return SubmitDeleteIngredResponse(
        status_code = status.HTTP_200_OK,
    )


@router.get("/ingredUnitConvList/{query_params}")
def fetch_ingred_unit_conv_list(ingred_id: int, user_id: int, db: Session = Depends(get_db)):

    ingred_service = IngredService(user_id, db)
    ingred_unit_conv_list = ingred_service.fetch_ingred_unit_conv_list(ingred_id)
    return ingred_unit_conv_list


@router.post("/submitAddIngredUnitConv", response_model=SubmitAddIngredUnitConvResponse)
async def submit_add_ingred_unit_conv(request: SubmitAddIngredUnitConvRequest, db: Session = Depends(get_db)):

    ingred_service = IngredService(request.user_id, db)
    new_ingred_unit_conv = ingred_service.add_ingred_unit_conv(request.ingred_id, request.from_unit_cd, request.conv_rate)
    return SubmitAddIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
        new_ingred_unit_conv = new_ingred_unit_conv
    )


@router.put("/submitEditIngredUnitConv", response_model=SubmitUpdateIngredUnitConvResponse)
async def submit_edit_ingred_unit_conv(request: SubmitUpdateIngredUnitConvRequest, db: Session = Depends(get_db)):

    ingred_service = IngredService(request.user_id, db)
    new_ingred_unit_conv = ingred_service.edit_ingred_unit_conv(request.ingred_unit_conv_id, request.ingred_id, request.from_unit_cd, request.conv_rate)
    return SubmitAddIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
        new_ingred_unit_conv = new_ingred_unit_conv,
    )


@router.delete("/submitDeleteIngredUnitConv/{query_params}", response_model=SubmitDeleteIngredUnitConvResponse)
async def submit_delete_ingred_unit_conv(ingred_unit_conv_id: int, db: Session = Depends(get_db)):

    ingred_service = IngredService(None, db)
    ingred_service.delete_ingred_unit_conv(ingred_unit_conv_id)
    return SubmitDeleteIngredUnitConvResponse(
        status_code = status.HTTP_200_OK,
    )
