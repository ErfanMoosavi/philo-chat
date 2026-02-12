from .message import Message
from .philosopher import Philosopher
from ..exceptions import BadRequestError
from ..utils.prompt_loading import load_prompt


class Chat:
    def __init__(self, name: str, philosopher: Philosopher) -> None:
        self.name = name
        self.philosopher = philosopher
        self.messages: list[Message] = []

    def complete_chat(
        self, input_text: str, username: str, name: str, age: str, chat_completer
    ) -> tuple[Message, Message]:
        cleaned_input = input_text.strip()

        if not cleaned_input:
            raise BadRequestError("Message cannot be empty")

        if self._is_first_message():
            prompt = load_prompt(cleaned_input, self.philosopher.name, name, age)
            prompt_msg = Message("user", username, prompt)
            self._add_message(prompt_msg)

        user_msg = Message("user", username, cleaned_input)
        self._add_message(user_msg)

        response = chat_completer.complete_chat(self.messages)
        ai_msg = Message("assistant", self.philosopher.name, response)
        self._add_message(ai_msg)

        return ai_msg, user_msg

    def get_history(self) -> list[Message]:
        return self.messages[1:]

    def _add_message(self, new_msg: Message) -> None:
        self.messages.append(new_msg)

    def _is_first_message(self) -> bool:
        return bool(not self.messages)
