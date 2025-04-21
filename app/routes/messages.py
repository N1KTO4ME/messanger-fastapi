from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database1 import SessionLocal, Message
from app.schemas import MessageResponse
from typing import List

router = APIRouter(prefix="/messages", tags=["messages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=List[MessageResponse])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
    return messages
