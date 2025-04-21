from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database1 import SessionLocal, User
from app.schemas import UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
