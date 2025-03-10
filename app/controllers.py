from sqlalchemy.orm import Session
from models import Conversation, Message
from schemas import ChatRequest
from google import genai
from google.genai import types

sys_instruct = "You are a persuasive AI assistant. Your goal is to stand your ground on a topic and engage in a persuasive discussion.(without being overly argumentative).1 to 3 sentences should be enough to make your point. You can also ask questions to engage the user in a conversation"

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
    db.commit()
    db.refresh(user_msg)

    # Fetch conversation history
    recent_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())  # Order by ID ascending for chronological order
        .all()
    )

    # Format history for Gemini API CORRECTLY
    history = [
        genai.types.Content(parts=[genai.types.Part(text=msg.message)], role=msg.role if msg.role == "user" else "model")
        for msg in recent_messages
    ]


    # Generate response using Gemini
    try:
        client = genai.Client(api_key="AIzaSyDJ3kZMTk9NqWYr163ZshpZ5FrgW5RDPvU")

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=history, #Send the whole history
        )
        bot_reply = response.text.strip() if response.text else "I have no response."
    except Exception as e:
        bot_reply = f"Error generating response: {str(e)}"

    # Store bot response
    bot_msg = Message(conversation_id=conversation_id, role="bot", message=bot_reply)
    db.add(bot_msg)

    db.commit()

    # Fetch last 5 messages for conversation history for return value. This is only for the return, and not used by the model.
    recent_messages_return = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(5)
        .all()
    )

    history_return = [{"role": msg.role, "message": msg.message} for msg in reversed(recent_messages_return)]

    return conversation_id, history_return