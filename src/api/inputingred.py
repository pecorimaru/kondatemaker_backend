from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from src.utils.apiutils import CamelModel
from src.crud import common as common_crud
from src.crud import inputingred as inputingred_crud
from src.db.session import get_db

import src.utils.dbutils as dbutils

router = APIRouter()

class SubmitAddBuyIngredRequest(CamelModel):
    ingred_nm: str
    qty: float
    unit_nm: str
    sales_area_nm: str
    user_id: int

class SubmitAddBuyIngredResponse(CamelModel):
    status_code: int
    message: str
    dict_buy_ingreds: dict


class UnitList(CamelModel):
    unit_cd: str
    unit_nm: str

class SalesArea(CamelModel):
    cd: str
    nm: str

class InitItems(CamelModel):
    unit_nm: Optional[str] = None
    sales_area_nm: Optional[str] = None

@router.get("/unitList")
def fetch_unit_list(db: Session = Depends(get_db)):
    
    app_consts = common_crud.get_app_consts("C0002", db)

    unit_list = []
    for app_const in app_consts:
        unit_list.append(UnitList(
            unit_cd=app_const.val,
            unit_nm=app_const.val_content
        ))

    print(unit_list)
    return unit_list

@router.get("/initItemsForIngred/{query_params}")
def fetch_init_items(ingred_nm:str, user_id: int, db: Session = Depends(get_db)):
    
    unit_nm = inputingred_crud.get_standard_unit_nm(ingred_nm, user_id, db)

    sales_area_nm = inputingred_crud.get_sales_area_nm(ingred_nm, user_id, db)

    init_items = InitItems(
        unit_nm = unit_nm,
        sales_area_nm = sales_area_nm
    )

    print(init_items)
    return init_items

@router.get("/salesAreaList")
def fetch_sales_area_list(db: Session = Depends(get_db)):
    
    app_consts = common_crud.get_app_consts("C0004", db)

    sales_area_list = []
    for app_const in app_consts:
        sales_area_list.append(SalesArea(
            cd = app_const.val,
            nm = app_const.val_content
        ))

    print(sales_area_list)
    return sales_area_list


@router.post("/submitAddBuyIngred", response_model=SubmitAddBuyIngredResponse)
async def submit_add_buy_ingred(request: SubmitAddBuyIngredRequest, db: Session = Depends(get_db)):


    new_buy_ingreds = inputingred_crud.create_buy_ingreds(request.ingred_nm, request.qty, request.unit_nm, request.sales_area_nm, request.user_id, db)
    
    dict_buy_ingreds = dbutils.to_dict(new_buy_ingreds) 

    return SubmitAddBuyIngredResponse(
        status_code = 200,
        message = "Success",
        dict_buy_ingreds = dict_buy_ingreds
    )


