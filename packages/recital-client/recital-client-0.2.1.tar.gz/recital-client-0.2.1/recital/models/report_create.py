import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportCreate")


@attr.s(auto_attribs=True)
class ReportCreate:
    """ Report schema to retrieve from POST methods. """

    name: str
    bkgd_task_id: Union[Unset, int] = UNSET
    expires_on: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        bkgd_task_id = self.bkgd_task_id
        expires_on: Union[Unset, str] = UNSET
        if not isinstance(self.expires_on, Unset):
            expires_on = self.expires_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if bkgd_task_id is not UNSET:
            field_dict["bkgd_task_id"] = bkgd_task_id
        if expires_on is not UNSET:
            field_dict["expires_on"] = expires_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        bkgd_task_id = d.pop("bkgd_task_id", UNSET)

        expires_on: Union[Unset, datetime.datetime] = UNSET
        _expires_on = d.pop("expires_on", UNSET)
        if not isinstance(_expires_on, Unset):
            expires_on = isoparse(_expires_on)

        report_create = cls(
            name=name,
            bkgd_task_id=bkgd_task_id,
            expires_on=expires_on,
        )

        report_create.additional_properties = d
        return report_create

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
