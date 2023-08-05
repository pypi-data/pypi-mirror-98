from enum import Enum


class ExtractTaskStatus(str, Enum):
    AUTO = "auto"
    SETUP = "setup"
    MANUAL = "manual"
    DONE = "done"
    ERROR = "error"

    def __str__(self) -> str:
        return str(self.value)
