from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AccessToken:
    """ Access token schema to output on refresh and login endpoints. """

    access_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if access_token is not UNSET:
            field_dict["access_token"] = access_token

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AccessToken":
        d = src_dict.copy()
        access_token = d.pop("access_token", UNSET)

        access_token = AccessToken(
            access_token=access_token,
        )

        access_token.additional_properties = d
        return access_token

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
