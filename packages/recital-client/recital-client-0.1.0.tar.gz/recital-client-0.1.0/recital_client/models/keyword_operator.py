from enum import Enum


class KeywordOperator(str, Enum):
    AND_ = "and"
    OR_ = "or"

    def __str__(self) -> str:
        return str(self.value)
