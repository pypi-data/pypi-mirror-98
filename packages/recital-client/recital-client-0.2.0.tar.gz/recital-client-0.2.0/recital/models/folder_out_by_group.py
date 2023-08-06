from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FolderOutByGroup")


@attr.s(auto_attribs=True)
class FolderOutByGroup:
    """ Folder schema to output from GET (by groups) method. """

    name: str
    id: int
    path: str
    write: bool
    parent_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        path = self.path
        write = self.write
        parent_id = self.parent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "path": path,
                "write": write,
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

        path = d.pop("path")

        write = d.pop("write")

        parent_id = d.pop("parent_id", UNSET)

        folder_out_by_group = cls(
            name=name,
            id=id,
            path=path,
            write=write,
            parent_id=parent_id,
        )

        folder_out_by_group.additional_properties = d
        return folder_out_by_group

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
