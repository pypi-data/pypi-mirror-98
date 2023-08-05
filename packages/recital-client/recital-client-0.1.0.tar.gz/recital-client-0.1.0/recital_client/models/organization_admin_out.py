from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class OrganizationAdminOut:
    """ Organization schema for admin output for POST methods. """

    email: str
    password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "OrganizationAdminOut":
        d = src_dict.copy()
        email = d.pop("email")

        password = d.pop("password")

        organization_admin_out = OrganizationAdminOut(
            email=email,
            password=password,
        )

        organization_admin_out.additional_properties = d
        return organization_admin_out

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
