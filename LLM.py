import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Loads variables from a local .env file when running locally.
# This is a no-op on Streamlit Cloud (no .env file present there).
load_dotenv()


def get_config(key: str):
    """
    Resolve a config value from either:
      1. Environment variables / .env file (local development), or
      2. st.secrets (Streamlit Cloud secrets panel).

    Streamlit Cloud does NOT read .env files, and values placed in its
    "Secrets" panel land in st.secrets, not in os.environ. Without this
    fallback, GROQ_API_KEY / BASE_URL / MODEL_NAME are silently None on
    Cloud unless you happen to also set them as raw environment
    variables. This function makes both paths work with zero extra code
    elsewhere in the project.
    """
    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets[key]
    except Exception:
        return None


API_KEY = get_config("GROQ_API_KEY")
BASE_URL = get_config("BASE_URL")
MODEL_NAME = get_config("MODEL_NAME")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Set it in a local .env file, "
        "or under Streamlit Cloud -> App settings -> Secrets."
    )

if not MODEL_NAME:
    raise ValueError(
        "MODEL_NAME not found. Set it in a local .env file, "
        "or under Streamlit Cloud -> App settings -> Secrets."
    )

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