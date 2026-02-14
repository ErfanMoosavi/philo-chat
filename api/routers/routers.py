from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from src.core import BadRequestError, LLMError, NotFoundError, PermissionDeniedError
from src.philo_chat import PhiloChat

from ..dependencies import get_philo_chat
from ..schema import (
    ChatCreate,
    ChatInput,
    ChatRef,
    UserAgeUpdate,
    UserCredentials,
    UserNameUpdate,
)

router = APIRouter(prefix="/philo-chat", tags=["philo-chat"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCredentials, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.signup(user.username, user.password)
        return {"message": "User created successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK)
def create_token(user: UserCredentials, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.login(user.username, user.password)
        return {"message": "Logged in successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/profile/logout", status_code=status.HTTP_200_OK)
def delete_token(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.logout()
        return {"message": "Logged out successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.delete("/profile/delete_account", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.delete_account()
        return {"message": "Account deleted successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.put("/users/{username}", status_code=status.HTTP_200_OK)
def update_name(data: UserNameUpdate, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.set_name(data.name)
        return {"message": "Set name successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.put("/users/{username}", status_code=status.HTTP_200_OK)
def update_age(data: UserAgeUpdate, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.set_age(data.age)
        return {"message": "Set age successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/profile/picture", status_code=status.HTTP_200_OK)
async def upload_profile_picture(
    file: UploadFile = File(...), pc: PhiloChat = Depends(get_philo_chat)
):
    try:
        pc.set_profile_picture(file.file, file.filename)
        return {"message": "Set profile picture successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/chats", status_code=status.HTTP_201_CREATED)
def create_chat(chat: ChatCreate, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.new_chat(chat.chat_name, chat.philosopher_id)
        return {"message": "Added chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/chats/{chat_name}/select", status_code=status.HTTP_200_OK)
def select_chat(chat: ChatRef, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.select_chat(chat.chat_name)
        return {"message": "Selected chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/chats", status_code=status.HTTP_200_OK)
def get_chats(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        chat_list = pc.list_chats()
        return chat_list

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/chats/exit", status_code=status.HTTP_200_OK)
def exit_chat(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.exit_chat()
        return {"message": "Exited chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete_chat/{chat_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_name: str, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.delete_chat(chat_name)
        return {"message": "Deleted chat successfully"}

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/chats/{chat_name}/messages", status_code=status.HTTP_200_OK)
def create_message(data: ChatInput, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        ai_msg, user_msg = pc.complete_chat(data.input_text)
        return ai_msg, user_msg

    except PermissionDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except LLMError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/philosophers", status_code=status.HTTP_200_OK)
def list_philosophers(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        philosophers = pc.list_philosophers()
        return philosophers

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
