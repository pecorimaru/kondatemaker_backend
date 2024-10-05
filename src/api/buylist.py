from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.crud import buylist as buylist_crud
from src.db.session import get_db

router = APIRouter()

class PutResponse(BaseModel):
    statusCode: int
    message: str

@router.get("/buyIngreds/{query_params}")
def fetch_toweek_recipes(user_id: int, db: Session = Depends(get_db)):
    
    buy_ingreds = buylist_crud.get_buy_ingreds(user_id, db)
    print(buy_ingreds)
    return buy_ingreds


class SwitchCompletionStateRequest(BaseModel):
    buy_ingreds_id: int
    flg: str

@router.put("/switchCompletionState", response_model=PutResponse)
async def refresh_toweek_plan(request: SwitchCompletionStateRequest, db: Session = Depends(get_db)):

    message = buylist_crud.update_buy_ingreds_bought_flg(request.buy_ingreds_id, request.flg,  db)

    return PutResponse(
        statusCode=200,
        message = message
    )
