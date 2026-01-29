import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. "
    "Answer clearly and concisely."
)
