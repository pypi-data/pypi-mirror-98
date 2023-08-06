from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RightsCreate")


@attr.s(auto_attribs=True)
class RightsCreate:
    """ Rights schema to receive from POST method. """

    group_id: int
    write: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        group_id = self.group_id
        write = self.write

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_id": group_id,
                "write": write,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        group_id = d.pop("group_id")

        write = d.pop("write")

        rights_create = cls(
            group_id=group_id,
            write=write,
        )

        rights_create.additional_properties = d
        return rights_create

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
