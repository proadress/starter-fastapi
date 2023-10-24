from fastapi import FastAPI, routing,Request,APIRouter
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import typing

auth =  APIRouter()

def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []

templates = Jinja2Templates(directory="templates")
templates.env.globals['get_flashed_messages'] = get_flashed_messages



@auth.get("/", response_class=HTMLResponse)
def home(request: Request):
    flash(request, "Login Successful", category="error")
    return templates.TemplateResponse("header.html", {"request": request})
