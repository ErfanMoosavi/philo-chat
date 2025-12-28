from datetime import datetime


class Message:
    def __init__(self, role: str, author: str, content: str):
        self.author = author
        self.role = role
        self.content = content
        self.time = datetime.now().strftime("%H:%M")
