from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.websockets import router as websocket_router
from app.routes.users import router as users_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(websocket_router)
app.include_router(users_router)

@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})
@app.get("/chat")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})