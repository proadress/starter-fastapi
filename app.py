from fastapi import FastAPI, routing,Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(debug=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
print(3)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    print(2)
    return templates.TemplateResponse("header.html", {"request": request})
