from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Message, User
from app.schemas import MessageCreate, MessageResponse
from typing import List

router = APIRouter(prefix="/messages", tags=["messages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    sender = db.query(User).filter(User.id == message.sender_id).first()
    receiver = db.query(User).filter(User.id == message.receiver_id).first() if message.receiver_id else None

    if not sender:
        raise HTTPException(status_code=404, detail="Отправитель не найден")
    if message.receiver_id and not receiver:
        raise HTTPException(status_code=404, detail="Получатель не найден")

    new_message = Message(sender_id=message.sender_id, receiver_id=message.receiver_id, content=message.content)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
