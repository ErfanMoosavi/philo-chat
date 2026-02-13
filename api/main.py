import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from shcemas import (
    ChatCreate,
    ChatInput,
    ChatRef,
    UserAgeUpdate,
    UserCredentials,
    UserNameUpdate,
)
from src.core import (
    BadRequestError,
    LLMError,
    NotFoundError,
    PermissionDeniedError,
)
from src.philo_chat import PhiloChat

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

pc = PhiloChat(base_url=base_url, api_key=openai_api_key, model_name=model_name)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Philosopher Chat API", "status": "running"}


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCredentials):
    try:
        pc.signup(user.username, user.password)
        return {"message": "User created successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserCredentials):
    try:
        pc.login(user.username, user.password)
        return {"message": "Logged in successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    try:
        pc.logout()
        return {"message": "Logged out successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.delete("/delete_account", status_code=status.HTTP_200_OK)
def delete_account():
    try:
        pc.delete_account()
        return {"message": "Account deleted successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.put("/set_name", status_code=status.HTTP_200_OK)
def set_name(data: UserNameUpdate):
    try:
        pc.set_name(data.name)
        return {"message": "Set name successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.put("/set_age", status_code=status.HTTP_200_OK)
def set_age(data: UserAgeUpdate):
    try:
        pc.set_age(data.age)
        return {"message": "Set age successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.post("/set_profile_picture", status_code=status.HTTP_200_OK)
async def set_profile_picture(file: UploadFile = File(...)):
    try:
        pc.set_profile_picture(file.file, file.filename)
        return {"message": "Set profile picture successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.post("/new_chat", status_code=status.HTTP_200_OK)
def new_chat(chat: ChatCreate):
    try:
        pc.new_chat(chat.chat_name, chat.philosopher_id)
        return {"message": "Added chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@app.post("/select_chat", status_code=status.HTTP_200_OK)
def select_chat(chat: ChatRef):
    try:
        pc.select_chat(chat.chat_name)
        return {"message": "Selected chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/chat_list", status_code=status.HTTP_200_OK)
def list_chats():
    try:
        chat_list = pc.list_chats()
        return chat_list

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put("/exit_chat", status_code=status.HTTP_200_OK)
def exit_chat():
    try:
        pc.exit_chat()
        return {"message": "Exited chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/delete_chat", status_code=status.HTTP_200_OK)
def delete_chat(chat: ChatRef):
    try:
        pc.delete_chat(chat.chat_name)
        return {"message": "Deleted chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/complete_chat", status_code=status.HTTP_200_OK)
def complete_chat(data: ChatInput):
    try:
        ai_msg, user_msg = pc.complete_chat(data.input_text)
        return ai_msg, user_msg

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except LLMError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/philosophers", status_code=status.HTTP_200_OK)
def list_philosophers():
    try:
        philosophers = pc.list_philosophers()
        return philosophers

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
