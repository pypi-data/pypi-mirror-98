import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.version import Version

T = TypeVar("T", bound="DocumentBookmarkCurrentVersion")


@attr.s(auto_attribs=True)
class DocumentBookmarkCurrentVersion:
    """ Document bookmark schema containing the current version info. """

    name: str
    item_id: int
    collection_id: int
    id: int
    created_on: datetime.datetime
    current_version: Version
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        item_id = self.item_id
        collection_id = self.collection_id
        id = self.id
        created_on = self.created_on.isoformat()

        current_version = self.current_version.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "item_id": item_id,
                "collection_id": collection_id,
                "id": id,
                "created_on": created_on,
                "current_version": current_version,
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

        current_version = Version.from_dict(d.pop("current_version"))

        document_bookmark_current_version = cls(
            name=name,
            item_id=item_id,
            collection_id=collection_id,
            id=id,
            created_on=created_on,
            current_version=current_version,
        )

        document_bookmark_current_version.additional_properties = d
        return document_bookmark_current_version

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
