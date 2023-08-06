import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="CollectionOutput")


@attr.s(auto_attribs=True)
class CollectionOutput:
    """ Document collection schema to output from a GET method. """

    name: str
    id: int
    user_id: int
    created_on: datetime.datetime
    modified_on: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        user_id = self.user_id
        created_on = self.created_on.isoformat()

        modified_on = self.modified_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "user_id": user_id,
                "created_on": created_on,
                "modified_on": modified_on,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        user_id = d.pop("user_id")

        created_on = isoparse(d.pop("created_on"))

        modified_on = isoparse(d.pop("modified_on"))

        collection_output = cls(
            name=name,
            id=id,
            user_id=user_id,
            created_on=created_on,
            modified_on=modified_on,
        )

        collection_output.additional_properties = d
        return collection_output

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
