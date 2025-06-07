from __future__ import annotations

from .image import Image


class Messages:
    def __init__(
            self, 
            messages:list[dict[str, str | Image]]|"Messages"|None = None
        ):

        if isinstance(messages, Messages):
            self.messages = messages.messages.copy()
        elif isinstance(messages, list):
            self.messages = messages
        else:
            self.messages = []

    def add_message(self, role: str, content: str | Image) -> None:
        self.messages.append({"role": role, "content": content})

    def get_list(self, delete_system_role: bool = False) -> list[dict[str, str]]:
        messages = []

        for message in self.messages:
            if delete_system_role and message["role"] == "system":
                continue
            if isinstance(message["content"], Image):
                content = str(message["content"])
            else:
                content = message["content"]
            messages.append({"role": message["role"], "content": content})

        return messages