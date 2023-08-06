from enum import Enum


class MetadataType(str, Enum):
    NUMBER = "number"
    BOOL = "bool"
    DATE = "date"
    DATERANGE = "daterange"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
