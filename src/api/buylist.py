from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.crud import buylist as buylist_crud
from src.db.session import get_db
from src.utils.apiutils import CamelModel

router = APIRouter()

class SwitchCompletionStateResponse(CamelModel):
    status_code: int
    message: str

class SwitchCompletionStateRequest(CamelModel):
    buy_ingreds_id: int
    flg: str

@router.get("/buyIngreds/{query_params}")
def fetch_toweek_recipes(user_id: int, db: Session = Depends(get_db)):
    
    buy_ingreds_list = buylist_crud.get_buy_ingreds_list(user_id, db)
    print(buy_ingreds_list)
    return buy_ingreds_list


@router.put("/switchCompletionState", response_model=SwitchCompletionStateResponse)
async def refresh_toweek_plan(request: SwitchCompletionStateRequest, db: Session = Depends(get_db)):

    message = buylist_crud.update_buy_ingreds_bought_flg(request.buy_ingreds_id, request.flg,  db)

    return SwitchCompletionStateResponse(
        statusCode=200,
        message = message
    )
