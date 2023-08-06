from enum import Enum


class ValueType(str, Enum):
    REGEX = "regex"
    NER = "ner"

    def __str__(self) -> str:
        return str(self.value)
