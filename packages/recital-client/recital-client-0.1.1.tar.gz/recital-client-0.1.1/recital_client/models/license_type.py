from enum import Enum


class LicenseType(str, Enum):
    DEMO = "demo"
    POC = "poc"
    PROD = "prod"

    def __str__(self) -> str:
        return str(self.value)
