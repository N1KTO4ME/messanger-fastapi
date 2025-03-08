from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.websockets import router as websocket_router

app = FastAPI()

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(websocket_router)

@app.get("/")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
