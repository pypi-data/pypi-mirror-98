from enum import Enum


class UserLanguage(str, Enum):
    EN = "en"
    FR = "fr"

    def __str__(self) -> str:
        return str(self.value)
