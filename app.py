from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from aws import login_account
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    # 从模板渲染上下文传递数据
    data = {"message": "Hello, World!"}
    return templates.TemplateResponse("base.html", {"request": request, "data": data})


# # JWT 配置
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"


# # FastAPI JWT 配置
# class Settings:
#     authjwt_secret_key = SECRET_KEY
#     authjwt_algorithm = ALGORITHM


# # authjwt = AuthJWT(settings=Settings)


# # 用户认证模型
# class UserCredentials(OAuth2PasswordRequestForm):
#     def validate(self):
#         if not login_account(self.username, self.password):
#             raise HTTPException(status_code=400, detail="Wrong username or password")


# # 登录端点
# @app.get("/login")
# async def login(credentials: UserCredentials):
#     #access_token = authjwt.create_access_token(subject=credentials.username)
#     return templates.TemplateResponse("base.html")


# # 注销端点
# @app.post("/logout")
# async def logout(authorize: AuthJWT = Depends()):
#     # 在 FastAPI JWT 中，JWT 令牌通常是无状态的，不需要显式注销
#     # 如果你需要实现 JWT 令牌的黑名单，你可以在服务器端维护一个黑名单列表
#     return templates.TemplateResponse("base.html")
