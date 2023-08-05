from enum import Enum


class Product(str, Enum):
    SEARCH = "search"
    EXTRACT = "extract"

    def __str__(self) -> str:
        return str(self.value)
