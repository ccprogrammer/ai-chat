import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_ai_reply(user_message: str) -> str:
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
    )

    return response.choices[0].message.content
