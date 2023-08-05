from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class TwoFactorBaseCredentials:
    """ Two factor base credentials schema. """

    username: str
    password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "TwoFactorBaseCredentials":
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        two_factor_base_credentials = TwoFactorBaseCredentials(
            username=username,
            password=password,
        )

        two_factor_base_credentials.additional_properties = d
        return two_factor_base_credentials

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
