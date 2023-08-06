from enum import Enum


class KeywordsDirection(str, Enum):
    BEFORE = "before"
    AFTER = "after"
    AROUND = "around"

    def __str__(self) -> str:
        return str(self.value)
