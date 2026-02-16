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
