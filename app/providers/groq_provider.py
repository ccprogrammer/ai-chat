from openai import OpenAI
from app.core.config import GROQ_API_KEY
from app.providers.model_registry import MODEL_REGISTRY

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

def generate_chat_completion(messages: list, model_key: str) -> str:
    model_name = MODEL_REGISTRY[model_key]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
