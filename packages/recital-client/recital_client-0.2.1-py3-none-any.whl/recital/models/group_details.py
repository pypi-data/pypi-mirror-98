import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.folder_details import FolderDetails

T = TypeVar("T", bound="GroupDetails")


@attr.s(auto_attribs=True)
class GroupDetails:
    """ Group schema to output from GET groups/details. """

    name: str
    id: int
    org_id: int
    created_on: datetime.datetime
    read_rights: List[FolderDetails]
    write_rights: List[FolderDetails]
    n_users: int
    n_docs: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        org_id = self.org_id
        created_on = self.created_on.isoformat()

        read_rights = []
        for read_rights_item_data in self.read_rights:
            read_rights_item = read_rights_item_data.to_dict()

            read_rights.append(read_rights_item)

        write_rights = []
        for write_rights_item_data in self.write_rights:
            write_rights_item = write_rights_item_data.to_dict()

            write_rights.append(write_rights_item)

        n_users = self.n_users
        n_docs = self.n_docs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "org_id": org_id,
                "created_on": created_on,
                "read_rights": read_rights,
                "write_rights": write_rights,
                "n_users": n_users,
                "n_docs": n_docs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        org_id = d.pop("org_id")

        created_on = isoparse(d.pop("created_on"))

        read_rights = []
        _read_rights = d.pop("read_rights")
        for read_rights_item_data in _read_rights:
            read_rights_item = FolderDetails.from_dict(read_rights_item_data)

            read_rights.append(read_rights_item)

        write_rights = []
        _write_rights = d.pop("write_rights")
        for write_rights_item_data in _write_rights:
            write_rights_item = FolderDetails.from_dict(write_rights_item_data)

            write_rights.append(write_rights_item)

        n_users = d.pop("n_users")

        n_docs = d.pop("n_docs")

        group_details = cls(
            name=name,
            id=id,
            org_id=org_id,
            created_on=created_on,
            read_rights=read_rights,
            write_rights=write_rights,
            n_users=n_users,
            n_docs=n_docs,
        )

        group_details.additional_properties = d
        return group_details

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
