from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern="^[a-z0-9]+$")
    password: str = Field(..., min_length=4, max_length=30)


class UserNameUpdate(BaseModel):
    name: str = Field(..., min_length=3, max_length=20, pattern="^[A-Za-z ]+$")


class UserAgeUpdate(BaseModel):
    age: int = Field(..., gt=10, lt=100)


class ChatCreate(BaseModel):
    chat_name: str = Field(..., min_length=3, max_length=20)
    philosopher_id: int = Field(ge=0, le=4)


class ChatRef(BaseModel):
    chat_name: str = Field(..., min_length=3, max_length=20)


class ChatInput(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=2000)
