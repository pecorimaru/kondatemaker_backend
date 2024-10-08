import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

from src.db.session import SessionLocal
from src.api.login import router as login_router
from src.api.home import router as home_router
from src.api.buylist import router as buylist_router
from src.api.inputingred import router as inputingred_router


app = FastAPI()

load_dotenv()
client_url = os.getenv("CLIENT_URL")
# CORSを設定して、Reactからのリクエストを許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=[client_url],  # ReactのサーバーURL
    # allow_origins=["https://kondatemaker.mydns.jp"],  # ReactのサーバーURL
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico")
async def favicon():
    file_path = os.path.join(r"backend\static", "favicon.ico")
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # ファビコンが見つからない場合
    return FileResponse(os.path.join("static", "default_favicon.ico"))


app.include_router(login_router, prefix="/api")  # ログイン画面
app.include_router(home_router, prefix="/api/home")   # ホーム画面
app.include_router(buylist_router, prefix="/api/buyList")   # 買い物リスト画面
app.include_router(inputingred_router, prefix="/api/inputIngred")   # 買い物リスト画面

# テストコメント

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)