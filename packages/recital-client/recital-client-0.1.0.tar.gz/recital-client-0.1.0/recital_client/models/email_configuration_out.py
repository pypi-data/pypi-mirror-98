from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class EmailConfigurationOut:
    """ Email configuration schema for endpoints return. """

    signature: str
    org_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signature = self.signature
        org_id = self.org_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signature": signature,
                "org_id": org_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "EmailConfigurationOut":
        d = src_dict.copy()
        signature = d.pop("signature")

        org_id = d.pop("org_id")

        email_configuration_out = EmailConfigurationOut(
            signature=signature,
            org_id=org_id,
        )

        email_configuration_out.additional_properties = d
        return email_configuration_out

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
