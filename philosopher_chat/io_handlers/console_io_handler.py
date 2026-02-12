class ConsoleIOHandler:
    def display_message(self, message: str) -> None:
        print(message)

    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def display_chat_message(self, message: str) -> None:
        print("-" * 50)
        print(message)

    def display_philosophers(self, philosophers: list) -> None:
        for i, philosopher in enumerate(philosophers, start=1):
            print(f"{i}. {philosopher.name}")

    def display_chats_list(self, chats: list) -> None:
        for chat in chats:
            print(f"{chat.name}\tPhilosopher-> {chat.philosopher.name}")
