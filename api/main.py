from fastapi import FastAPI
import os

from dotenv import load_dotenv
from ..philosopher_chat.core.system import System

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

app = FastAPI()
pc = System(base_url=base_url, api_key=openai_api_key, model_name=model_name)
