from sqlalchemy.orm import Session
from models import Conversation, Message
from schemas import ChatRequest

# Handles message storage and bot response generation
def handle_chat(request: ChatRequest, db: Session):
    user_message = request.message
    conversation_id = request.conversation_id

    if not user_message:
        return None, "Message is required"

    # Start a new conversation if `conversation_id` is not provided
    if not conversation_id:
        new_convo = Conversation()
        db.add(new_convo)
        db.commit()
        db.refresh(new_convo)
        conversation_id = new_convo.id

    # Store user message
    user_msg = Message(conversation_id=conversation_id, role="user", message=user_message)
    db.add(user_msg)

    # Generate bot response (dummy response for now)
    bot_reply = f"Bot response to: {user_message}"
    bot_msg = Message(conversation_id=conversation_id, role="bot", message=bot_reply)
    db.add(bot_msg)

    db.commit()

    # Fetch last 5 messages for conversation history
    recent_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(5)
        .all()
    )

    history = [{"role": msg.role, "message": msg.message} for msg in reversed(recent_messages)]

    return conversation_id, history
