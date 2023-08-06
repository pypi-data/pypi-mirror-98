from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="OrganizationAdminIn")


@attr.s(auto_attribs=True)
class OrganizationAdminIn:
    """ Organization schema to admin input for POST methods. """

    first_name: str
    last_name: str
    email: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name
        last_name = self.last_name
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        email = d.pop("email")

        organization_admin_in = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        organization_admin_in.additional_properties = d
        return organization_admin_in

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
