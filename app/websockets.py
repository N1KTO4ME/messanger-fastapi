from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Chat, Message, User
from typing import Dict

router = APIRouter()

# Активные соединения WebSocket
active_connections: Dict[str, WebSocket] = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.websocket("/ws/{username}/{receiver}")
async def websocket_endpoint(websocket: WebSocket, username: str, receiver: str, db: Session = Depends(get_db)):
    await websocket.accept()
    print(f"Запрос: username={username} ({type(username)}), receiver={receiver} ({type(receiver)})")

    chat_key = f"{username}-{receiver}" if receiver != "global" else "global"
    active_connections[chat_key] = websocket

    print(f"Новое подключение: {username} -> {receiver}")

    # Проверяем, существует ли пользователь
    sender = db.query(User).filter(User.id == username).first()
    recipient = db.query(User).filter(User.id == receiver).first() if receiver != "global" else None

    if not sender:
        await websocket.send_text("Ошибка: отправитель не найден")
        return

    if receiver != "global" and not recipient:
        await websocket.send_text("Ошибка: получатель не найден")
        return

    # Определяем или создаем чат
    if receiver == "global":
        chat = None  # Глобальный чат без chat_id
    else:
        chat = db.query(Chat).filter(
            ((Chat.user1_id == sender.id) & (Chat.user2_id == recipient.id)) |
            ((Chat.user1_id == recipient.id) & (Chat.user2_id == sender.id))
        ).first()

        if not chat:
            chat = Chat(user1_id=sender.id, user2_id=recipient.id)
            db.add(chat)
            db.commit()


    # Отправляем историю сообщений
    chat_id = chat.id if chat else None
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()

    for msg in messages:
        sender_info = db.query(User).filter(User.id == msg.sender_id).first()
        sender_name = sender_info.username if sender_info else "Неизвестный"
        await websocket.send_text(f"{sender_name}: {msg.content}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Получено сообщение от {username}: {data}")

            new_message = Message(
                chat_id=None if receiver == "global" else chat.id,
                sender_id=None if receiver == "global" else sender.id,
                content=data
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            print(f"Сообщение сохранено в БД: {new_message.id}, {new_message.content}")

            for conn_key, conn in active_connections.items():
                if conn_key == chat_key or conn_key == f"{receiver}-{username}":
                    print(f"Отправка {username} -> {conn_key}: {data}")
                    await conn.send_text(f"{username}: {data}")

    except WebSocketDisconnect:
        print(f"Соединение закрыто: {username} -> {receiver}")
        del active_connections[chat_key]