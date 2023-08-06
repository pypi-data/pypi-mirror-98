from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="MetadataId")


@attr.s(auto_attribs=True)
class MetadataId:
    """ Metadata schema to represent a metadata id """

    metadata_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata_id = self.metadata_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_id": metadata_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata_id = d.pop("metadata_id")

        metadata_id = cls(
            metadata_id=metadata_id,
        )

        metadata_id.additional_properties = d
        return metadata_id

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
