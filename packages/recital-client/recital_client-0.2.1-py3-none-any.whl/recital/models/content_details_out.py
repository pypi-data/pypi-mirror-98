from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.group_out import GroupOut

T = TypeVar("T", bound="ContentDetailsOut")


@attr.s(auto_attribs=True)
class ContentDetailsOut:
    """ Content details schema to output from GET method. """

    id: int
    name: str
    groups: List[GroupOut]
    total_folders: int
    total_files: int
    total_size: int
    num_defined_metadata: int
    num_indexed_files: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()

            groups.append(groups_item)

        total_folders = self.total_folders
        total_files = self.total_files
        total_size = self.total_size
        num_defined_metadata = self.num_defined_metadata
        num_indexed_files = self.num_indexed_files

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "groups": groups,
                "total_folders": total_folders,
                "total_files": total_files,
                "total_size": total_size,
                "num_defined_metadata": num_defined_metadata,
                "num_indexed_files": num_indexed_files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = GroupOut.from_dict(groups_item_data)

            groups.append(groups_item)

        total_folders = d.pop("total_folders")

        total_files = d.pop("total_files")

        total_size = d.pop("total_size")

        num_defined_metadata = d.pop("num_defined_metadata")

        num_indexed_files = d.pop("num_indexed_files")

        content_details_out = cls(
            id=id,
            name=name,
            groups=groups,
            total_folders=total_folders,
            total_files=total_files,
            total_size=total_size,
            num_defined_metadata=num_defined_metadata,
            num_indexed_files=num_indexed_files,
        )

        content_details_out.additional_properties = d
        return content_details_out

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
