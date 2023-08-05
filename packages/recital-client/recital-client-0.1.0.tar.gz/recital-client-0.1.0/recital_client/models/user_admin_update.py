from typing import Any, Dict, List, Union, cast

import attr

from ..models.user_role import UserRole
from ..models.user_status import UserStatus
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class UserAdminUpdate:
    """ User schema to receive from PUT /{user_id}/admin endpoint. """

    role: Union[Unset, UserRole] = UNSET
    org_contact: Union[Unset, bool] = UNSET
    status: Union[Unset, UserStatus] = UNSET
    group_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role: Union[Unset, UserRole] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role

        org_contact = self.org_contact
        status: Union[Unset, UserStatus] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status

        group_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.group_ids, Unset):
            group_ids = self.group_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if org_contact is not UNSET:
            field_dict["org_contact"] = org_contact
        if status is not UNSET:
            field_dict["status"] = status
        if group_ids is not UNSET:
            field_dict["group_ids"] = group_ids

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "UserAdminUpdate":
        d = src_dict.copy()
        role = None
        _role = d.pop("role", UNSET)
        if _role is not None:
            role = UserRole(_role)

        org_contact = d.pop("org_contact", UNSET)

        status = None
        _status = d.pop("status", UNSET)
        if _status is not None:
            status = UserStatus(_status)

        group_ids = cast(List[int], d.pop("group_ids", UNSET))

        user_admin_update = UserAdminUpdate(
            role=role,
            org_contact=org_contact,
            status=status,
            group_ids=group_ids,
        )

        user_admin_update.additional_properties = d
        return user_admin_update

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
