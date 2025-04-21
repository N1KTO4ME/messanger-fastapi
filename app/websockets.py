from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Chat, ChatMember, Message, User
from typing import Dict

router = APIRouter()

active_connections: Dict[int, Dict[int, WebSocket]] = {}
# active_connections[chat_id][user_id] = websocket


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    # 1) Примем подключение
    await websocket.accept()

    # 2) Проверим, что чат существует
    chat = db.query(Chat).filter_by(chat_id=chat_id).first()
    if not chat:
        await websocket.close(code=1008)
        return

    # 3) Проверим, что пользователь есть и входит в чат
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        await websocket.close(code=1008)
        return

    membership = (
        db.query(ChatMember)
        .filter_by(chat_id=chat_id, user_id=user_id)
        .first()
    )
    if not membership:
        # автоматически добавить в общий чат или запретить
        await websocket.close(code=1008)
        return

    # 4) Зарегистрируем соединение
    active_connections.setdefault(chat_id, {})[user_id] = websocket

    # 5) Отправим историю
    msgs = (
        db.query(Message)
        .filter_by(chat_id=chat_id)
        .order_by(Message.timestamp)
        .all()
    )
    for m in msgs:
        await websocket.send_text(f"{m.sender.full_name}: {m.content}")

    try:
        while True:
            text = await websocket.receive_text()

            # 6) Сохраним в БД
            msg = Message(chat_id=chat_id, sender_id=user_id, content=text)
            db.add(msg)
            db.commit()
            db.refresh(msg)

            # 7) Рассылим всем участникам чата
            for uid, ws in active_connections[chat_id].items():
                await ws.send_text(f"{user.full_name}: {text}")

    except WebSocketDisconnect:
        # удаляем сокет
        active_connections[chat_id].pop(user_id, None)
