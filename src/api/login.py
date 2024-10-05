from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.crud import login as login_crud
from src.db.session import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    statusCode: int
    detail: dict

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = login_crud.get_user(request.email, db)
    if user:
        if user.password == request.password:
            return LoginResponse(
                statusCode=200,
                detail={
                    "id": user.user_id,
                    "name": user.user_nm,
                    "message": "Login Successful"
                }
            )

    raise HTTPException(
        status_code=401,
        detail={
            "id": None,
            "name": "",
            "message": "Invalid username or password"
        }
    )