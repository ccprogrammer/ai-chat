from app.services.memory_service import add_message, get_conversation
from app.providers.groq_provider import generate_chat_completion
from app.core.config import SYSTEM_PROMPT

def chat_with_ai(user_id: str, user_message: str, model: str) -> str:
    add_message(user_id, "user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(get_conversation(user_id))

    ai_reply = generate_chat_completion(messages, model)

    add_message(user_id, "assistant", ai_reply)
    return ai_reply
