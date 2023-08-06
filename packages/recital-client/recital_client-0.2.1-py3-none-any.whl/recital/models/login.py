from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.password_policy_expected import PasswordPolicyExpected
from ..models.user_out import UserOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="Login")


@attr.s(auto_attribs=True)
class Login:
    """ Login schema to output from POST /login endpoint. """

    user: UserOut
    access_token: Union[Unset, str] = UNSET
    refresh_token: Union[Unset, str] = UNSET
    update_pwd_token: Union[Unset, str] = UNSET
    policy: Union[PasswordPolicyExpected, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user = self.user.to_dict()

        access_token = self.access_token
        refresh_token = self.refresh_token
        update_pwd_token = self.update_pwd_token
        policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
            }
        )
        if access_token is not UNSET:
            field_dict["access_token"] = access_token
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if update_pwd_token is not UNSET:
            field_dict["update_pwd_token"] = update_pwd_token
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user = UserOut.from_dict(d.pop("user"))

        access_token = d.pop("access_token", UNSET)

        refresh_token = d.pop("refresh_token", UNSET)

        update_pwd_token = d.pop("update_pwd_token", UNSET)

        policy: Union[PasswordPolicyExpected, Unset] = UNSET
        _policy = d.pop("policy", UNSET)
        if not isinstance(_policy, Unset):
            policy = PasswordPolicyExpected.from_dict(_policy)

        login = cls(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            update_pwd_token=update_pwd_token,
            policy=policy,
        )

        login.additional_properties = d
        return login

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
