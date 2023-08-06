import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FileItemOut")


@attr.s(auto_attribs=True)
class FileItemOut:
    """ File item schema to output from GET methods. """

    folder_id: int
    display_name: str
    id: int
    org_id: int
    name: str
    uuid: str
    created_on: datetime.datetime
    updated_on: datetime.datetime
    idx_task_id: Union[Unset, int] = UNSET
    current_version_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self.folder_id
        display_name = self.display_name
        id = self.id
        org_id = self.org_id
        name = self.name
        uuid = self.uuid
        created_on = self.created_on.isoformat()

        updated_on = self.updated_on.isoformat()

        idx_task_id = self.idx_task_id
        current_version_id = self.current_version_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folder_id": folder_id,
                "display_name": display_name,
                "id": id,
                "org_id": org_id,
                "name": name,
                "uuid": uuid,
                "created_on": created_on,
                "updated_on": updated_on,
            }
        )
        if idx_task_id is not UNSET:
            field_dict["idx_task_id"] = idx_task_id
        if current_version_id is not UNSET:
            field_dict["current_version_id"] = current_version_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_id = d.pop("folder_id")

        display_name = d.pop("display_name")

        id = d.pop("id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        uuid = d.pop("uuid")

        created_on = isoparse(d.pop("created_on"))

        updated_on = isoparse(d.pop("updated_on"))

        idx_task_id = d.pop("idx_task_id", UNSET)

        current_version_id = d.pop("current_version_id", UNSET)

        file_item_out = cls(
            folder_id=folder_id,
            display_name=display_name,
            id=id,
            org_id=org_id,
            name=name,
            uuid=uuid,
            created_on=created_on,
            updated_on=updated_on,
            idx_task_id=idx_task_id,
            current_version_id=current_version_id,
        )

        file_item_out.additional_properties = d
        return file_item_out

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
