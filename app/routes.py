from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ChatRequest, ChatResponse
from database import get_db
from controllers import handle_chat

router = APIRouter()

# Chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    conversation_id, history = handle_chat(request, db)

    if history is None:
        raise HTTPException(status_code=400, detail="Message is required")

    return {"conversation_id": conversation_id, "message": history}
