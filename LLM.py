import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def chat(messages: list) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()