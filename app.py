from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware

middleware = [Middleware(SessionMiddleware, secret_key="super-secret")]
app = FastAPI(middleware=middleware, debug=True)
app.mount("/static/", StaticFiles(directory="static", html=True), name="static")
#load page
from auth import auth
app.include_router(auth)
