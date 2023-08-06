import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FolderOut")


@attr.s(auto_attribs=True)
class FolderOut:
    """ Folder schema to output from GET methods. """

    name: str
    id: int
    org_id: int
    path: str
    created_on: datetime.datetime
    updated_on: datetime.datetime
    parent_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        org_id = self.org_id
        path = self.path
        created_on = self.created_on.isoformat()

        updated_on = self.updated_on.isoformat()

        parent_id = self.parent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "org_id": org_id,
                "path": path,
                "created_on": created_on,
                "updated_on": updated_on,
            }
        )
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        org_id = d.pop("org_id")

        path = d.pop("path")

        created_on = isoparse(d.pop("created_on"))

        updated_on = isoparse(d.pop("updated_on"))

        parent_id = d.pop("parent_id", UNSET)

        folder_out = cls(
            name=name,
            id=id,
            org_id=org_id,
            path=path,
            created_on=created_on,
            updated_on=updated_on,
            parent_id=parent_id,
        )

        folder_out.additional_properties = d
        return folder_out

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
