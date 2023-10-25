from fastapi import Request, APIRouter, Form, HTTPException
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import boto3
auth = APIRouter()

dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('ill-ruby-firefly-gownCyclicDB')


templates = Jinja2Templates(directory="templates")


@auth.get("/login", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth.post("/login/process")
async def login(email: str = Form(...),password: str = Form(...)):
    print(password)
    if email == "2@1":
        # 如果电子邮件正确，可以在此执行登录操作
        return {"message": "success"}
    else:
        # 如果电子邮件不正确，返回错误消息
        return {"message": "Invalid email"}


@auth.get("/qrcode", response_class=HTMLResponse)
async def qrcode(request: Request):
    return templates.TemplateResponse("qrcode.html", {"request": request})


@auth.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@auth.get("/logout")
async def logout():
    return RedirectResponse(url="/login")
