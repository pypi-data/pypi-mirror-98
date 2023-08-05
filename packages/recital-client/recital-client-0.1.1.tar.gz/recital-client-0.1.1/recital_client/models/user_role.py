from enum import Enum


class UserRole(str, Enum):
    BASIC = "basic"
    ORGADMIN = "orgadmin"
    SYSADMIN = "sysadmin"
    SERVICE = "service"
    BASICORGADMINSYSADMINSERVICE = "basic+orgadmin+sysadmin+service"
    SYSADMINORGADMIN = "sysadmin+orgadmin"
    BASICORGADMINSYSADMIN = "basic+orgadmin+sysadmin"
    BASICORGADMIN = "basic+orgadmin"
    SERVICESYSADMIN = "service+sysadmin"

    def __str__(self) -> str:
        return str(self.value)
