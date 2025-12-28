from .status import Status
from .message import Message
from .philosopher import Philosopher


class Chat:
    def __init__(self, name: str, philosopher: Philosopher):
        self.name = name
        self.philosopher = philosopher
        self.messages: list[Message] = []

    def complete_chat(
        self, input_text: str, username: str, prompt_loader, chat_completer
    ) -> tuple[Status, Message, Message]:
        cleaned_input = input_text.strip()
        if not cleaned_input:
            return Status.BAD_REQUEST, None

        if self._is_first_message():
            prompt = prompt_loader.load_prompts(cleaned_input, self.philosopher.name)
            prompt_msg = Message("user", username, prompt)
            self._add_message(prompt_msg)

        user_msg = Message("user", username, cleaned_input)
        self._add_message(user_msg)

        response = chat_completer.complete_chat(self.messages)
        ai_msg = Message("assistant", self.philosopher.name, response)
        self._add_message(ai_msg)

        return Status.SUCCESS, ai_msg, user_msg

    def get_history(self) -> list[Message]:
        return self.messages[1:]

    def _add_message(self, new_msg: Message) -> None:
        self.messages.append(new_msg)

    def _is_first_message(self) -> bool:
        return bool(not self.messages)
