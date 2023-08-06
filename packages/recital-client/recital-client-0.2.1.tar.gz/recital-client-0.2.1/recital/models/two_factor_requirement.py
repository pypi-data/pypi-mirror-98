from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TwoFactorRequirement")


@attr.s(auto_attribs=True)
class TwoFactorRequirement:
    """ Two factor autentication requirement schema. """

    user_id: int
    required: bool
    provisioning_uri: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        required = self.required
        provisioning_uri = self.provisioning_uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "required": required,
            }
        )
        if provisioning_uri is not UNSET:
            field_dict["provisioning_uri"] = provisioning_uri

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id")

        required = d.pop("required")

        provisioning_uri = d.pop("provisioning_uri", UNSET)

        two_factor_requirement = cls(
            user_id=user_id,
            required=required,
            provisioning_uri=provisioning_uri,
        )

        two_factor_requirement.additional_properties = d
        return two_factor_requirement

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
