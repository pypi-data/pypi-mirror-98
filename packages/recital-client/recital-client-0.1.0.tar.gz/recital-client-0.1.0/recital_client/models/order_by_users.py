from enum import Enum


class OrderByUsers(str, Enum):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    CREATED_ON = "created_on"

    def __str__(self) -> str:
        return str(self.value)
