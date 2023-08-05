from enum import Enum


class QuestionnaireStatus(str, Enum):
    AUTO = "auto"
    SETUP = "setup"
    DONE = "done"
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
