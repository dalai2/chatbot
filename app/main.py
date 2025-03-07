from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres_user:postgres_password@localhost:5432/chatdb")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Models
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "bot"
    message = Column(String)

    conversation = relationship("Conversation", backref="messages")

# Create tables
Base.metadata.create_all(bind=engine)

# API Setup
app = FastAPI()

# Request & Response Models
class ChatRequest(BaseModel):
    conversation_id: Optional[str]
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: list[dict]

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Chat API Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_message = request.message
    conversation_id = request.conversation_id

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    if not conversation_id:
        # Create a new conversation
        new_convo = Conversation()
        db.add(new_convo)
        db.commit()
        db.refresh(new_convo)
        conversation_id = new_convo.id

    # Save user message
    user_msg = Message(conversation_id=conversation_id, role="user", message=user_message)
    db.add(user_msg)

    # Generate bot response (dummy for now)
    bot_reply = f"Bot response to: {user_message}"
    bot_msg = Message(conversation_id=conversation_id, role="bot", message=bot_reply)
    db.add(bot_msg)

    db.commit()

    # Retrieve last 5 messages
    recent_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(5)
        .all()
    )

    history = [{"role": msg.role, "message": msg.message} for msg in reversed(recent_messages)]

    return {"conversation_id": conversation_id, "message": history}
