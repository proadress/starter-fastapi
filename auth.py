from fastapi import Request, APIRouter, Form, Depends
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import aws, User
from fastapi_login import LoginManager
from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

auth = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    secret: str = ""  # automatically taken from environment variable


DEFAULT_SETTINGS = Settings(_env_file=".env")
TOKEN_URL = "/auth/token"
manager = LoginManager(DEFAULT_SETTINGS.secret, TOKEN_URL)


@manager.user_loader()
def get_user(sid: str):
    return aws.check_item("user", sid)


@auth.get("/login", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth.get("/qrcode", response_class=HTMLResponse)
async def qrcode(request: Request):
    return templates.TemplateResponse("qrcode.html", {"request": request})


@auth.get("/", response_class=HTMLResponse)
async def home(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("home.html", {"request": request})


@auth.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@auth.get("/getData")
async def getData():
    return aws.scan_all()


@auth.post("/deleteData")
async def deleteData(pk: str = Form(...), sk: str = Form(...)):
    return aws.delete_user(pk, sk)


@auth.post("/createUser")
async def createData(sid: str = Form(...), password: str = Form(...), username: str = Form(...)):
    print(sid, password, username)
    user = User(pk="user", sk=sid, password=password, username=username)
    response = aws.create_user(user)
    return {"message": response}


@auth.post(TOKEN_URL)
def login(data: OAuth2PasswordRequestForm = Depends()):
    sid = data.username
    password = data.password
    user = get_user(sid)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user["password"]:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data=dict(sub=sid))
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get("/logout")
async def logout():
    resp = RedirectResponse(url="/login", status_code=302)
    manager.set_cookie(resp, "")
    return resp
