from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

router = APIRouter()

# Список активных соединений
active_connections: Dict[int, WebSocket] = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Сообщение от {user_id}: {data}")

            # Рассылаем сообщение всем активным пользователям
            for uid, conn in active_connections.items():
                if uid != user_id:
                    await conn.send_text(f"Пользователь {user_id}: {data}")

    except WebSocketDisconnect:
        print(f"Пользователь {user_id} отключился")
        del active_connections[user_id]
