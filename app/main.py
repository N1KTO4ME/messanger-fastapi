from fastapi import FastAPI
from app.websockets import router as websocket_router
from app.database import init_db

app = FastAPI()

# Инициализация базы данных
init_db()

# Подключаем WebSocket
app.include_router(websocket_router)

@app.get("/")
def read_root():
    return {"message": "Сервер мессенджера работает!"}
