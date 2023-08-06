from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TwoFactorAuthentication")


@attr.s(auto_attribs=True)
class TwoFactorAuthentication:
    """ Policy base schema. """

    two_factor_enabled: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        two_factor_enabled = self.two_factor_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "two_factor_enabled": two_factor_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        two_factor_enabled = d.pop("two_factor_enabled")

        two_factor_authentication = cls(
            two_factor_enabled=two_factor_enabled,
        )

        two_factor_authentication.additional_properties = d
        return two_factor_authentication

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
