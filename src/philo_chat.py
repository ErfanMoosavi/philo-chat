import json
from pathlib import Path

from .core.entities.chat import Chat
from .core.entities.chat_completer import ChatCompleter
from .core.entities.message import Message
from .core.entities.philosopher import Philosopher
from .core.entities.user import User
from .core.exceptions import BadRequestError, NotFoundError, PermissionDeniedError


class PhiloChat:
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        self.chat_completer = ChatCompleter(base_url, api_key, model_name)
        self.users: dict[str, User] = {}
        self.philosophers: dict[int, Philosopher] = self._load_philosophers()
        self.logged_in_user: User | None = None

    def signup(self, username: str, password: str, name: str, age: int) -> None:
        if self.logged_in_user:
            raise PermissionDeniedError("You are already logged in")
        elif self._find_user(username):
            raise BadRequestError(f"Username {username} already taken")

        new_user = User(username, password, name, age)
        self.users[username] = new_user

    def login(self, username: str, password: str) -> None:
        user = self._find_user(username)

        if self.logged_in_user:
            raise PermissionDeniedError("You've already logged in")
        elif not user:
            raise NotFoundError("Username not found")
        elif user.password != password:
            raise PermissionDeniedError("Wrong password")

        self.logged_in_user = user

    def logout(self) -> None:
        if not self.logged_in_user:
            raise PermissionDeniedError("No user is logged in")

        self.logged_in_user = None

    def delete_account(self) -> None:
        if not self.logged_in_user:
            raise PermissionDeniedError("No user is logged in")

        del self.users[self.logged_in_user.username]
        self.logout()

    def new_chat(self, name: str, philosopher_id: int) -> None:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        philosopher = self._find_philosopher(philosopher_id)
        return self.logged_in_user.new_chat(name, philosopher)

    def select_chat(self, name: str) -> list[Message]:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        return self.logged_in_user.select_chat(name)

    def list_chats(self) -> list[Chat]:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        return self.logged_in_user.list_chats()

    def exit_chat(self) -> None:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        return self.logged_in_user.exit_chat()

    def delete_chat(self, name: str) -> None:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        return self.logged_in_user.delete_chat(name)

    def list_philosophers(self) -> list[Philosopher]:
        if not self.philosophers:
            raise NotFoundError("No philosopher found")

        return list(self.philosophers.values())

    def complete_chat(self, input_text: str) -> tuple[Message, Message]:
        if not self.logged_in_user:
            raise BadRequestError("No user is logged in")

        return self.logged_in_user.complete_chat(input_text, self.chat_completer)

    def _find_user(self, username: str) -> User | None:
        return self.users.get(username)

    def _find_philosopher(self, philosopher_id: int) -> Philosopher | None:
        return self.philosophers.get(philosopher_id)

    def _load_philosophers(self) -> dict[int, Philosopher]:
        data_dir = Path(__file__).parent / "data/philosophers.json"

        with open(data_dir, "r", encoding="utf-8") as f:
            raw_philosophers = json.load(f)

        philosophers = {}
        for p in raw_philosophers:
            philosophers[p["id"]] = Philosopher(p["id"], p["name"])
        return philosophers
