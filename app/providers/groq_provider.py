from openai import OpenAI
from app.core.config import GROQ_API_KEY

# Always use fast model (Llama 3.1 8B Instant)
GROQ_FAST_MODEL = "llama-3.1-8b-instant"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)


def generate_chat_completion(messages: list) -> str:
    response = client.chat.completions.create(
        model=GROQ_FAST_MODEL,
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content


TITLE_SYSTEM_PROMPT = (
    "You generate very short chat titles. Given a user message, reply with ONLY a title of 3-6 words "
    "that captures the topic. No quotes, no punctuation at the end, no explanation. Just the title."
)


def generate_chat_title(first_message: str) -> str:
    """Generate a short title from the user's first message (for new chats)."""
    response = client.chat.completions.create(
        model=GROQ_FAST_MODEL,
        messages=[
            {"role": "system", "content": TITLE_SYSTEM_PROMPT},
            {"role": "user", "content": first_message[:500]},  # avoid huge input
        ],
        temperature=0.3,
        max_tokens=30,
    )
    title = (response.choices[0].message.content or "").strip()
    return title[:80] if title else "New chat"  # cap length; fallback if empty
