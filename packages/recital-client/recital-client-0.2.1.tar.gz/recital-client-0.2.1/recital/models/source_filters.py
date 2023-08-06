from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="SourceFilters")


@attr.s(auto_attribs=True)
class SourceFilters:
    """ Source filters schema. """

    metadata_name: str
    folder_ids: List[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata_name = self.metadata_name
        folder_ids = self.folder_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_name": metadata_name,
                "folder_ids": folder_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata_name = d.pop("metadata_name")

        folder_ids = cast(List[int], d.pop("folder_ids"))

        source_filters = cls(
            metadata_name=metadata_name,
            folder_ids=folder_ids,
        )

        source_filters.additional_properties = d
        return source_filters

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
