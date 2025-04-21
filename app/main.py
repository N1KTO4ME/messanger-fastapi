from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.websockets import router as websocket_router
from app.routes.users import router as users_router
from app.routes.chats import router as chats_router  # новый

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(websocket_router)

@app.get("/")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# Dependency для роутов, если нужно
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
