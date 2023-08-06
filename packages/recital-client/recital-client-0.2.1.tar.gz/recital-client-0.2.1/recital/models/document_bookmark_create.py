from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DocumentBookmarkCreate")


@attr.s(auto_attribs=True)
class DocumentBookmarkCreate:
    """ Document bookmark schema to receive from a POST method. """

    name: str
    item_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        item_id = self.item_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "item_id": item_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        item_id = d.pop("item_id")

        document_bookmark_create = cls(
            name=name,
            item_id=item_id,
        )

        document_bookmark_create.additional_properties = d
        return document_bookmark_create

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
