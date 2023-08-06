from enum import Enum


class SourceType(str, Enum):
    FOLDERS = "folders"
    METADATA = "metadata"

    def __str__(self) -> str:
        return str(self.value)
