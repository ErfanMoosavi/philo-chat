from fastapi import FastAPI
import os

from dotenv import load_dotenv
from philosopher_chat.core.system import System

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

app = FastAPI()
pc = System(base_url=base_url, api_key=openai_api_key, model_name=model_name)


@app.get("/")
def root():
    return {"message": "Philosopher Chat API", "status": "running"}


@app.get("/philosophers")
def get_philosophers():
    philosophers = pc.get_philosophers()
    return philosophers


@app.post("/signup")
def signup(username: str, password: str):
    pc.signup(username, password)


@app.post("/login")
def login(username: str, password: str):
    pc.login(username, password)


@app.post("/logout")
def logout():
    pc.logout()


@app.delete("/delete_account")
def delete_account():
    pc.delete_account()
