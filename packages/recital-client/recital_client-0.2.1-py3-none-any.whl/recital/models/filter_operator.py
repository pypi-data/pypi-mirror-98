from enum import Enum


class FilterOperator(str, Enum):
    EQ = "eq"
    NEQ = "neq"
    IN_ = "in"
    NIN = "nin"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    BTW = "btw"
    NBTW = "nbtw"
    WTHN = "wthn"
    NWTHN = "nwthn"
    CTN = "ctn"
    NCTN = "nctn"
    INT = "int"
    NINT = "nint"

    def __str__(self) -> str:
        return str(self.value)
