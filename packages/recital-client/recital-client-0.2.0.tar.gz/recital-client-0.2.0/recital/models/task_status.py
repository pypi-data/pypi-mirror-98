from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    ERROR = "error"
    DONE = "done"
    CANCELED = "canceled"
    WAIT_FOR_VALIDATION = "wait_for_validation"

    def __str__(self) -> str:
        return str(self.value)
