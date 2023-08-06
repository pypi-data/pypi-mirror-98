from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyPostUserLoginApiV1Login_Post")


@attr.s(auto_attribs=True)
class BodyPostUserLoginApiV1Login_Post:
    """  """

    username: str
    password: str
    totp: Union[Unset, str] = UNSET
    new_password: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        password = self.password
        totp = self.totp
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
            }
        )
        if totp is not UNSET:
            field_dict["totp"] = totp
        if new_password is not UNSET:
            field_dict["new_password"] = new_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        totp = d.pop("totp", UNSET)

        new_password = d.pop("new_password", UNSET)

        body_post_user_login_api_v1_login_post = cls(
            username=username,
            password=password,
            totp=totp,
            new_password=new_password,
        )

        body_post_user_login_api_v1_login_post.additional_properties = d
        return body_post_user_login_api_v1_login_post

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
