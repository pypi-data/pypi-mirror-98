from enum import Enum


class UserStatus(str, Enum):
    OPEN = "open"
    EXPIRED = "expired"
    BLOCKED = "blocked"

    def __str__(self) -> str:
        return str(self.value)
