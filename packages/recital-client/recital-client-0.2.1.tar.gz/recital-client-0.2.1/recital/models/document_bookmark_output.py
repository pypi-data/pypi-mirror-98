import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="DocumentBookmarkOutput")


@attr.s(auto_attribs=True)
class DocumentBookmarkOutput:
    """ Document bookmark schema to output from a GET method. """

    name: str
    item_id: int
    collection_id: int
    id: int
    created_on: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        item_id = self.item_id
        collection_id = self.collection_id
        id = self.id
        created_on = self.created_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "item_id": item_id,
                "collection_id": collection_id,
                "id": id,
                "created_on": created_on,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        item_id = d.pop("item_id")

        collection_id = d.pop("collection_id")

        id = d.pop("id")

        created_on = isoparse(d.pop("created_on"))

        document_bookmark_output = cls(
            name=name,
            item_id=item_id,
            collection_id=collection_id,
            id=id,
            created_on=created_on,
        )

        document_bookmark_output.additional_properties = d
        return document_bookmark_output

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
