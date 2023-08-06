from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DisplayPolicyUpdate")


@attr.s(auto_attribs=True)
class DisplayPolicyUpdate:
    """ Display policy update schema. """

    see_explorer: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        see_explorer = self.see_explorer

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "see_explorer": see_explorer,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        see_explorer = d.pop("see_explorer")

        display_policy_update = cls(
            see_explorer=see_explorer,
        )

        display_policy_update.additional_properties = d
        return display_policy_update

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
