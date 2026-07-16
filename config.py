import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY") or st.secrets["API_KEY"]

BASE_URL = os.getenv("BASE_URL") or st.secrets["BASE_URL"]
MODEL_NAME = os.getenv("MODEL_NAME") or st.secrets["MODEL_NAME"]

GEOCODING_URL = os.getenv("GEOCODING_URL") or st.secrets["GEOCODING_URL"]
WEATHER_URL = os.getenv("WEATHER_URL") or st.secrets["WEATHER_URL"]