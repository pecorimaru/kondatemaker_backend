import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
import os

from app.api.login import router as login_router
from app.api.home import router as home_router
from app.api.buy import router as buylist_router
from app.api.ingred_form import router as ingred_form_router
from app.api.ingred import router as ingred_router
from app.api.recipe import router as recipe_router
from app.api.recipe_form import router as recipe_form_router
from app.api.menu_plan import router as menu_plan_router
from app.api.app_const import router as const_router
from app.api.setting import router as setting_router
from app.core.global_event_handlers import global_event_handlers

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
client_url_list = os.getenv("CLIENT_URL_LIST").split(";")



# CORSを設定して、Reactからのリクエストを許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=client_url_list,  # ReactのサーバーURL
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


global_event_handlers(app)
app.include_router(login_router, prefix="/api/login")
app.include_router(home_router, prefix="/api/home")
app.include_router(buylist_router, prefix="/api/buy")
app.include_router(ingred_form_router, prefix="/api/ingredForm")
app.include_router(ingred_router, prefix="/api/ingred")
app.include_router(recipe_router, prefix="/api/recipe")
app.include_router(recipe_form_router, prefix="/api/recipeForm")
app.include_router(menu_plan_router, prefix="/api/menuPlan")
app.include_router(const_router, prefix="/api/const")
app.include_router(setting_router, prefix="/api/setting")
# テストコメント

if __name__ == "__main__":

    config = uvicorn.Config(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        access_log=False  # アクセスログを無効化
    )
    server = uvicorn.Server(config)
    server.run()