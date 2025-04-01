from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from datetime import datetime

# Базовый класс для моделей SQLAlchemy
class Base(DeclarativeBase):
    pass

# Подключение к базе данных SQLite
DATABASE_URL = "sqlite:///./messenger.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    messages_sent = relationship("Message", back_populates="sender", cascade="all, delete-orphan")


# Модель чата (диалога между двумя пользователями)
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


# Модель сообщения
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="messages_sent")
    chat = relationship("Chat", back_populates="messages")


# Функция для создания таблиц в БД
def init_db():
    """Создаёт таблицы в БД, если их нет."""
    Base.metadata.create_all(bind=engine)

# Вызываем создание таблиц
init_db()