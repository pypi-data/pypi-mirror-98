from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.timezone import Timezone
from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCreate")


@attr.s(auto_attribs=True)
class UserCreate:
    """ User schema to receive from POST method. """

    org_id: int
    first_name: str
    last_name: str
    email: str
    role: UserRole
    timezone: Timezone
    language: Union[Unset, None] = UNSET
    org_contact: Union[Unset, bool] = False
    group_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org_id = self.org_id
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        role = self.role.value

        timezone = self.timezone.value

        language = None

        org_contact = self.org_contact
        group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.group_ids, Unset):
            group_ids = self.group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_id": org_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "role": role,
                "timezone": timezone,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language
        if org_contact is not UNSET:
            field_dict["org_contact"] = org_contact
        if group_ids is not UNSET:
            field_dict["group_ids"] = group_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org_id = d.pop("org_id")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        email = d.pop("email")

        role = UserRole(d.pop("role"))

        timezone = Timezone(d.pop("timezone"))

        language = None

        org_contact = d.pop("org_contact", UNSET)

        group_ids = cast(List[int], d.pop("group_ids", UNSET))

        user_create = cls(
            org_id=org_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            timezone=timezone,
            language=language,
            org_contact=org_contact,
            group_ids=group_ids,
        )

        user_create.additional_properties = d
        return user_create

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
