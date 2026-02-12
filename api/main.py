import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status

from philo_chat.src.core.exceptions import (
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
)
from philo_chat.src.philo_chat import PhiloChat

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

app = FastAPI()
pc = PhiloChat(base_url=base_url, api_key=openai_api_key, model_name=model_name)


@app.get("/")
def root():
    return {"message": "Philosopher Chat API", "status": "running"}


@app.get("/philosophers", status_code=status.HTTP_200_OK)
def list_philosophers():
    try:
        philosophers = pc.list_philosophers()
        return philosophers
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No philosophers found"
        )


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(username: str, password: str):
    try:
        pc.signup(username, password)
        return {"message": "User created successfully"}
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You are already logged in"
        )
    except BadRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {username} already taken",
        )


@app.post("/login", status_code=status.HTTP_200_OK)
def login(username: str, password: str):
    try:
        pc.login(username, password)
        return {"message": "Logged in successfully"}
    except PermissionDeniedError as e:
        if "already logged in" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password"
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found"
        )


@app.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    try:
        pc.logout()
        return {"message": "Logged out successfully"}
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No user is logged in"
        )


@app.delete("/delete_account", status_code=status.HTTP_200_OK)
def delete_account():
    try:
        pc.delete_account()
        return {"message": "Account deleted successfully"}
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No user is logged in"
        )
