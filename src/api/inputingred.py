from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from src.crud import common as common_crud
from src.crud import inputingred as inputingred_crud
from src.db.session import get_db

import src.utils.dbutils as dbutils

router = APIRouter()

class SubmitRequest(BaseModel):
    ingredNm: str
    qty: float
    unitNm: str
    salesAreaNm: str
    userId: int

class SubmitResponse(BaseModel):
    statusCode: int
    detail: dict


class UnitList(BaseModel):
    unitCd: str
    unitNm: str

class SalesArea(BaseModel):
    cd: str
    nm: str

class InitItems(BaseModel):
    unitNm: Optional[str] = None
    salesAreaNm: Optional[str] = None

@router.get("/unitList")
def fetch_unit_list(db: Session = Depends(get_db)):
    
    app_consts = common_crud.get_app_const("C0002", db)

    unit_list = []
    for app_const in app_consts:
        unit_list.append(UnitList(
            unitCd=app_const.val,
            unitNm=app_const.val_content
        ))

    print(unit_list)
    return unit_list

@router.get("/initItemsForIngred/{query_params}")
def fetch_init_unit_nm(ingredNm:str, userId: int, db: Session = Depends(get_db)):
    
    unit_nm = inputingred_crud.get_standard_unit_nm(ingredNm, userId, db)

    sales_area_nm = inputingred_crud.get_sales_area_nm(ingredNm, userId, db)

    init_items = InitItems(
        unitNm = unit_nm,
        salesAreaNm = sales_area_nm
    )

    print(init_items)
    return init_items

@router.get("/salesAreaList")
def fetch_unit_list(db: Session = Depends(get_db)):
    
    app_consts = common_crud.get_app_const("C0004", db)

    sales_area_list = []
    for app_const in app_consts:
        sales_area_list.append(SalesArea(
            cd = app_const.val,
            nm = app_const.val_content
        ))

    print(sales_area_list)
    return sales_area_list


@router.post("/submit", response_model=SubmitResponse)
async def submit(request: SubmitRequest, db: Session = Depends(get_db)):


    new_buy_ingreds = inputingred_crud.create_buy_ingreds(request.ingredNm, request.qty, request.unitNm, request.salesAreaNm, request.userId, db)
    
    dict_buy_ingreds = dbutils.to_dict(new_buy_ingreds) 

    return SubmitResponse(
        statusCode = 200,
        detail = dict_buy_ingreds
    )
