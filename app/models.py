import uuid
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres_user:postgres_password@localhost:5432/chatdb")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Conversation Model
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))

# Message Model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "bot"
    message = Column(String)

    conversation = relationship("Conversation", backref="messages")

# Create tables in the database
Base.metadata.create_all(bind=engine)
