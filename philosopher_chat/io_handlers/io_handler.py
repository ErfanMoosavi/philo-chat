from abc import ABC, abstractmethod


class IOHandler(ABC):
    @abstractmethod
    def display_message(self, message: str) -> None:
        pass

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def display_chat_message(self, message: str) -> None:
        pass

    @abstractmethod
    def display_philosophers_list(self, philosophers: list) -> None:
        pass

    @abstractmethod
    def display_chats_list(self, chats: list) -> None:
        pass


class ConsoleIOHandler(IOHandler):
    def display_message(self, message: str) -> None:
        print(message)

    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def display_chat_message(self, message: str) -> None:
        print("-" * 50)
        print(message)

    def display_philosophers_list(self, philosophers: list) -> None:
        for i, philosopher in enumerate(philosophers, start=1):
            print(f"{i}. {philosopher.name}")

    def display_chats_list(self, chats: list) -> None:
        for chat in chats:
            print(f"{chat.name}\tPhilosopher-> {chat.philosopher.name}")
