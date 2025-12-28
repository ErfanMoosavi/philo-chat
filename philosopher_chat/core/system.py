import os
import json

from .chat_completer import ChatCompleter
from .prompt_loader import PromptLoader
from .user import User
from .philosopher import Philosopher
from .chat import Chat
from .message import Message
from .status import Status


class System:
    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.prompt_loader = PromptLoader()
        self.chat_completer = ChatCompleter(base_url, api_key, model_name)
        self.users: dict[str, User] = {}
        self.philosophers: dict[int, Philosopher] = self._load_philosophers()
        self.logged_in_user: User | None = None

    def signup(self, username: str, password: str) -> Status:
        if self.logged_in_user:
            return Status.PERMISSION_DENIED
        elif self._find_user(username):
            return Status.BAD_REQUEST

        new_user = User(username, password)
        self.users[username] = new_user
        return Status.SUCCESS

    def login(self, username: str, password: str) -> Status:
        user = self._find_user(username)

        if self.logged_in_user:
            return Status.PERMISSION_DENIED
        elif not user:
            return Status.NOT_FOUND
        elif user.password != password:
            return Status.PERMISSION_DENIED

        self.logged_in_user = user
        return Status.SUCCESS

    def logout(self) -> Status:
        if not self.logged_in_user:
            return Status.PERMISSION_DENIED

        self.logged_in_user = None
        return Status.SUCCESS

    def delete_account(self) -> Status:
        if not self.logged_in_user:
            return Status.PERMISSION_DENIED

        del self.users[self.logged_in_user.username]
        self.logout()
        return Status.SUCCESS

    def new_chat(self, name: str, philosopher_id: int) -> Status:
        if not self.logged_in_user:
            return Status.BAD_REQUEST

        philosopher = self._find_philosopher(philosopher_id)
        return self.logged_in_user.new_chat(name, philosopher)

    def select_chat(self, name: str) -> tuple[Status, list[Message]]:
        if not self.logged_in_user:
            return Status.BAD_REQUEST

        return self.logged_in_user.select_chat(name)

    def list_chats(self) -> tuple[Status, list[Chat]]:
        if not self.logged_in_user:
            return Status.BAD_REQUEST, []

        return self.logged_in_user.list_chats()

    def exit_chat(self) -> Status:
        if not self.logged_in_user:
            return Status.BAD_REQUEST

        return self.logged_in_user.exit_chat()

    def delete_chat(self, name: str) -> Status:
        if not self.logged_in_user:
            return Status.BAD_REQUEST

        return self.logged_in_user.delete_chat(name)

    def list_philosophers(self) -> tuple[Status, list[Philosopher]]:
        if not self.philosophers:
            return Status.NOT_FOUND, []

        return Status.SUCCESS, list(self.philosophers.values())

    def complete_chat(self, input_text: str) -> tuple[Status, Message, Message]:
        if not self.logged_in_user:
            return Status.BAD_REQUEST

        return self.logged_in_user.complete_chat(
            input_text, self.prompt_loader, self.chat_completer
        )

    def _find_user(self, username: str) -> User | None:
        return self.users.get(username)

    def _find_philosopher(self, philosopher_id: int) -> Philosopher | None:
        return self.philosophers.get(philosopher_id)

    def _load_philosophers(self) -> dict[int, Philosopher]:
        path = os.path.join(
            os.path.dirname(__file__), "..", "data", "philosophers.json"
        )
        path = os.path.abspath(path)
        with open(path, "r", encoding="utf-8") as f:
            raw_philosophers = json.load(f)

        philosophers = {}
        for p in raw_philosophers:
            philosophers[p["id"]] = Philosopher(p["id"], p["name"])
        return philosophers
