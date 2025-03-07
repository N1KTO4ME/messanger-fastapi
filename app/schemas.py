from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Позволяет автоматически преобразовывать SQLAlchemy-объекты

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: Optional[int] = None  # None — публичное сообщение
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: Optional[int]
    content: str

    class Config:
        from_attributes = True
