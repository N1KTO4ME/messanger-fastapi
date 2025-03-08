from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Message, User
from app.schemas import MessageCreate
from typing import Dict

router = APIRouter()

# Активные соединения WebSocket
active_connections: Dict[int, WebSocket] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections[user_id] = websocket

    # Отправляем историю сообщений
    messages = db.query(Message).filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
    for msg in messages:
        await websocket.send_text(f"[История] {msg.sender_id} -> {msg.receiver_id}: {msg.content}")

    try:
        while True:
            data = await websocket.receive_text()

            # Сохраняем сообщение в базе данных
            new_message = Message(sender_id=user_id, receiver_id=None, content=data)
            db.add(new_message)
            db.commit()

            # Рассылаем сообщение всем
            for uid, conn in active_connections.items():
                await conn.send_text(f"{user_id}: {data}")

    except WebSocketDisconnect:
        del active_connections[user_id]
