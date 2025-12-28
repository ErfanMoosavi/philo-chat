from openai import OpenAI

from .message import Message


class ChatCompleter:
    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name

    def complete_chat(self, messages: list[Message]) -> str:
        completion_messages = [self._msg_to_dict(msg) for msg in messages]

        completion = self.client.chat.completions.create(
            model=self.model_name, messages=completion_messages
        )
        return completion.choices[0].message.content.strip()

    def _msg_to_dict(self, msg: Message) -> dict[str, str]:
        return {"role": msg.role, "content": msg.content}
