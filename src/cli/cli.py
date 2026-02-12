import os
import sys
from enum import Enum

from dotenv import load_dotenv

from .console_io_handler import ConsoleIOHandler
from ..philo_chat import PhiloChat


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


class PhiloChatCLI:
    SUCCESS = "Success"

    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        self.system = PhiloChat(base_url, api_key, model_name)
        self.io = ConsoleIOHandler()
        self.help_menu = "Available commands:\n" + "\n".join(
            [f"\t-{command.value}" for command in Commands]
        )

    def run(self) -> None:
        self.io.display_message(
            "Welcome to Philosopher Chat!\nCommands? Type 'help' and see what's possible"
        )

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
        return f"[{msg.time}] {msg.author} ->\n{msg.content}"

    def _handle_command(self, command: str) -> str:
        if command == Commands.SIGNUP.value:
            return self._handle_signup()
        elif command == Commands.LOGIN.value:
            return self._handle_login()
        elif command == Commands.LOGOUT.value:
            return self._handle_logout()
        elif command == Commands.DELETE_ACCOUNT.value:
            return self._handle_delete_account()
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
        try:
            username = self.io.get_input("Enter your username: ")
            password = self.io.get_input("Enter your password: ")
            name = self.io.get_input("Enter your name: ")
            age = self.io.get_input("Enter your age: ")
            self.system.signup(username, password, name, age)
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_login(self) -> str:
        try:
            username = self.io.get_input("Enter your username: ")
            password = self.io.get_input("Enter your password: ")
            self.system.login(username, password)
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_logout(self) -> str:
        try:
            self.system.logout()
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_delete_account(self) -> str:
        try:
            self.system.delete_account()
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_new_chat(self) -> str:
        try:
            chat_name = self.io.get_input("Enter the chat name: ")
            philosophers_list = self.system.list_philosophers()

            self.io.display_philosophers_list(philosophers_list)

            philosopher_id = (
                int(self.io.get_input("Choose a philosopher by number: ")) - 1
            )
            if philosopher_id < 0 or philosopher_id >= len(philosophers_list):
                return "Invalid choice."

            # Convert list index to actual philosopher ID
            actual_philosopher_id = list(self.system.philosophers.keys())[
                philosopher_id
            ]
            self.system.new_chat(chat_name, actual_philosopher_id)
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_select_chat(self) -> str:
        name = self.io.get_input("Enter the chat name: ")
        return self._handle_chat_session(name)

    def _handle_chat_session(self, name: str) -> str:
        try:
            all_messages = self.system.select_chat(name)

            # Display chat history
            for msg in all_messages:
                self.io.display_chat_message(self._format_message(msg))

            # Chat loop
            while (
                self.system.logged_in_user and self.system.logged_in_user.selected_chat
            ):
                input_text = self.io.get_input(
                    "Enter your message (type 'exit_chat' to leave): "
                )
                if input_text == Commands.EXIT_CHAT.value:
                    self.system.exit_chat()
                    break

                ai_msg, user_msg = self.system.complete_chat(input_text)

                self.io.display_chat_message(self._format_message(user_msg))
                self.io.display_chat_message(self._format_message(ai_msg))

            return "Exited chat."

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_list_chats(self) -> str:
        try:
            chats = self.system.list_chats()
            self.io.display_chats_list(chats)

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_delete_chat(self) -> str:
        try:
            name = self.io.get_input("Enter the chat name: ")
            self.system.delete_chat(name)
            return self.SUCCESS

        except Exception as e:
            self.io.display_message(str(e))

    def _handle_list_philosophers(self) -> str:
        try:
            philosophers_list = self.system.list_philosophers()
            self.io.display_philosophers_list(philosophers_list)

        except Exception as e:
            self.io.display_message(str(e))


def main():
    """Entry point for the philo-chat console script."""

    load_dotenv()
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not all([base_url, api_key, model_name]):
        print("Missing environment variables. Create a .env file with:")
        print("BASE_URL=your_url")
        print("OPENAI_API_KEY=your_key")
        print("MODEL_NAME=your_model")
        sys.exit(1)

    # Run the app
    pcli = PhiloChatCLI(base_url, api_key, model_name)
    pcli.run()


if __name__ == "__main__":
    main()
