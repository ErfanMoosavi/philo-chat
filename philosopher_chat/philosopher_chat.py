from enum import Enum

from .core.system import System
from .core.status import Status
from .core.io_handler import ConsoleIOHandler


class Commands(Enum):
    SIGNUP = "signup"
    LOGIN = "login"
    LOGOUT = "logout"
    DELETE_ACCOUNT = "delete_account"
    NEW_CHAT = "new_chat"
    SELECT_CHAT = "select_chat"
    LIST_CHATS = "list_chats"
    EXIT_CHAT = "exit_chat"
    DELETE_CHAT = "delete_chat"
    LIST_PHILOSOPHERS = "list_philosophers"
    HELP = "help"
    EXIT = "exit"


class PhilosopherChat:
    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.system = System(base_url, api_key, model_name)
        self.io = ConsoleIOHandler()
        self.help_menu = "Available commands:\n" + "\n".join(
            [f"\t-{command.value}" for command in Commands]
        )

    def run(self):
        self.io.display_message("Welcome to Philosopher Chat!")
        self.io.display_message(self.help_menu)

        while True:
            command = self.io.get_input("Please enter the command: ")
            result = self._handle_command(command)

            if result == "EXIT":
                break
            elif result == "HELP":
                self.io.display_message(self.help_menu)
            elif result:
                self.io.display_message(result)

    def _format_message(self, msg) -> str:
        return f"[{msg.time}] {msg.author} →\n{msg.content}"

    def _handle_command(self, command: str) -> str:
        if command == Commands.SIGNUP.value:
            return self._handle_signup()
        elif command == Commands.LOGIN.value:
            return self._handle_login()
        elif command == Commands.LOGOUT.value:
            return self.system.logout().value
        elif command == Commands.DELETE_ACCOUNT.value:
            return self.system.delete_account().value
        elif command == Commands.NEW_CHAT.value:
            return self._handle_new_chat()
        elif command == Commands.SELECT_CHAT.value:
            return self._handle_select_chat()
        elif command == Commands.LIST_CHATS.value:
            return self._handle_list_chats()
        elif command == Commands.DELETE_CHAT.value:
            return self._handle_delete_chat()
        elif command == Commands.LIST_PHILOSOPHERS.value:
            return self._handle_list_philosophers()
        elif command == Commands.HELP.value:
            return "HELP"
        elif command == Commands.EXIT.value:
            return "EXIT"
        else:
            return "Please enter a valid command."

    def _handle_signup(self) -> str:
        username = self.io.get_input("Enter your username: ")
        password = self.io.get_input("Enter your password: ")
        return self.system.signup(username, password).value

    def _handle_login(self) -> str:
        username = self.io.get_input("Enter your username: ")
        password = self.io.get_input("Enter your password: ")
        return self.system.login(username, password).value

    def _handle_new_chat(self) -> str:
        chat_name = self.io.get_input("Enter the chat name: ")

        status, philosophers_list = self.system.list_philosophers()
        if status != Status.SUCCESS:
            return "No philosophers found."

        self.io.display_philosophers_list(philosophers_list)

        try:
            philosopher_id = (
                int(self.io.get_input("Choose a philosopher by number: ")) - 1
            )
            if philosopher_id < 0 or philosopher_id >= len(philosophers_list):
                return "Invalid choice."

            # Convert list index to actual philosopher ID
            actual_philosopher_id = list(self.system.philosophers.keys())[
                philosopher_id
            ]
        except (ValueError, IndexError):
            return "Invalid input. Please enter a valid number."

        return self.system.new_chat(chat_name, actual_philosopher_id).value

    def _handle_select_chat(self) -> str:
        name = self.io.get_input("Enter the chat name: ")
        return self._handle_chat_session(name)

    def _handle_chat_session(self, name: str) -> str:
        status, all_messages = self.system.select_chat(name)
        if status != Status.SUCCESS:
            return status.value

        # Display chat history
        for msg in all_messages:
            self.io.display_chat_message(self._format_message(msg))

        # Chat loop
        while self.system.logged_in_user and self.system.logged_in_user.selected_chat:
            input_text = self.io.get_input(
                "Enter your message (type 'exit_chat' to leave): "
            )
            if input_text == Commands.EXIT_CHAT.value:
                self.system.exit_chat()
                break

            status, ai_msg, user_msg = self.system.complete_chat(input_text)
            if status == Status.SUCCESS:
                self.io.display_chat_message(self._format_message(user_msg))
                self.io.display_chat_message(self._format_message(ai_msg))
            else:
                self.io.display_message(f"Error: {status.value}")

        return "Exited chat."

    def _handle_list_chats(self) -> str:
        status, chats = self.system.list_chats()
        if status == Status.SUCCESS:
            self.io.display_chats_list(chats)
        return status.value

    def _handle_delete_chat(self) -> str:
        name = self.io.get_input("Enter the chat name: ")
        return self.system.delete_chat(name).value

    def _handle_list_philosophers(self) -> str:
        status, philosophers_list = self.system.list_philosophers()
        if status == Status.SUCCESS:
            self.io.display_philosophers_list(philosophers_list)
        return status.value
