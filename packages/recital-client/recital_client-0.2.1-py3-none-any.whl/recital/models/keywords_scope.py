from enum import Enum


class KeywordsScope(str, Enum):
    CHUNK = "chunk"
    PAGE = "page"

    def __str__(self) -> str:
        return str(self.value)
