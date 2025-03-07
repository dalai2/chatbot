from typing import Optional, List
from pydantic import BaseModel

# Request Model
class ChatRequest(BaseModel):
    conversation_id: Optional[str]
    message: str

# Response Model
class ChatResponse(BaseModel):
    conversation_id: str
    message: List[dict]
