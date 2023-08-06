from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.timezone import Timezone
from ..models.user_language import UserLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserAccountUpdate")


@attr.s(auto_attribs=True)
class UserAccountUpdate:
    """ User schema to receive from PUT /account endpoint. """

    email: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    timezone: Union[Unset, Timezone] = UNSET
    language: Union[Unset, UserLanguage] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        timezone: Union[Unset, Timezone] = UNSET
        if not isinstance(self.timezone, Unset):
            timezone = self.timezone

        language: Union[Unset, UserLanguage] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        timezone: Union[Unset, Timezone] = UNSET
        _timezone = d.pop("timezone", UNSET)
        if not isinstance(_timezone, Unset):
            timezone = Timezone(_timezone)

        language: Union[Unset, UserLanguage] = UNSET
        _language = d.pop("language", UNSET)
        if not isinstance(_language, Unset):
            language = UserLanguage(_language)

        user_account_update = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
            timezone=timezone,
            language=language,
        )

        user_account_update.additional_properties = d
        return user_account_update

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
