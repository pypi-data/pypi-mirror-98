from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.group_import_report import GroupImportReport
from ..models.user_identity import UserIdentity

T = TypeVar("T", bound="ImportReport")


@attr.s(auto_attribs=True)
class ImportReport:
    """ Import report data. """

    created_users: List[UserIdentity]
    existing_users: List[UserIdentity]
    created_groups: List[GroupImportReport]
    existing_groups: List[GroupImportReport]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_users = []
        for created_users_item_data in self.created_users:
            created_users_item = created_users_item_data.to_dict()

            created_users.append(created_users_item)

        existing_users = []
        for existing_users_item_data in self.existing_users:
            existing_users_item = existing_users_item_data.to_dict()

            existing_users.append(existing_users_item)

        created_groups = []
        for created_groups_item_data in self.created_groups:
            created_groups_item = created_groups_item_data.to_dict()

            created_groups.append(created_groups_item)

        existing_groups = []
        for existing_groups_item_data in self.existing_groups:
            existing_groups_item = existing_groups_item_data.to_dict()

            existing_groups.append(existing_groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_users": created_users,
                "existing_users": existing_users,
                "created_groups": created_groups,
                "existing_groups": existing_groups,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_users = []
        _created_users = d.pop("created_users")
        for created_users_item_data in _created_users:
            created_users_item = UserIdentity.from_dict(created_users_item_data)

            created_users.append(created_users_item)

        existing_users = []
        _existing_users = d.pop("existing_users")
        for existing_users_item_data in _existing_users:
            existing_users_item = UserIdentity.from_dict(existing_users_item_data)

            existing_users.append(existing_users_item)

        created_groups = []
        _created_groups = d.pop("created_groups")
        for created_groups_item_data in _created_groups:
            created_groups_item = GroupImportReport.from_dict(created_groups_item_data)

            created_groups.append(created_groups_item)

        existing_groups = []
        _existing_groups = d.pop("existing_groups")
        for existing_groups_item_data in _existing_groups:
            existing_groups_item = GroupImportReport.from_dict(existing_groups_item_data)

            existing_groups.append(existing_groups_item)

        import_report = cls(
            created_users=created_users,
            existing_users=existing_users,
            created_groups=created_groups,
            existing_groups=existing_groups,
        )

        import_report.additional_properties = d
        return import_report

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
