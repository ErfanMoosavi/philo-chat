from ..exceptions import BadRequestError, NotFoundError
from .chat import Chat
from .message import Message
from .philosopher import Philosopher


class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.name = "Not Provided"
        self.age = "Not Provided"
        self.chats: dict[str, Chat] = {}
        self.selected_chat: Chat | None = None

    def set_name(self, name: str) -> None:
        self.name = name

    def set_age(self, age: int) -> None:
        self.age = age

    def new_chat(self, name: str, philosopher: Philosopher) -> None:
        if self._find_chat(name):
            raise BadRequestError("Chat already exists")

        new_chat = Chat(name, philosopher)
        self.chats[name] = new_chat

    def select_chat(self, name: str) -> list[Message]:
        chat = self._find_chat(name)

        if not chat:
            raise NotFoundError("Chat not found")

        self.selected_chat = chat
        return self.selected_chat.get_history()

    def list_chats(self) -> list[Chat]:
        if not self.chats:
            raise NotFoundError("No chats found")

        return list(self.chats.values())

    def exit_chat(self) -> None:
        if not self.selected_chat:
            raise BadRequestError("No chats selected")

        self.selected_chat = None

    def delete_chat(self, name: str) -> None:
        chat = self._find_chat(name)

        if not chat:
            raise NotFoundError("Chat not found")

        if self.selected_chat == chat:
            self.selected_chat = None
        del self.chats[name]

    def complete_chat(self, input_text: str, chat_completer) -> tuple[Message, Message]:
        if not self.selected_chat:
            raise BadRequestError("No chats selected")

        return self.selected_chat.complete_chat(
            input_text, self.username, self.name, self.age, chat_completer
        )

    def _find_chat(self, name: str) -> Chat | None:
        return self.chats.get(name)
