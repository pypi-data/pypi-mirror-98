from enum import Enum


class ExtractType(str, Enum):
    PARAGRAPH = "paragraph"
    VALUE = "value"
    QUESTION = "question"
    QUESTIONNAIRE = "questionnaire"

    def __str__(self) -> str:
        return str(self.value)
