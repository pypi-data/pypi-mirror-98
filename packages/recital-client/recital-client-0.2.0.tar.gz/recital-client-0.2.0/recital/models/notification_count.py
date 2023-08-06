from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationCount")


@attr.s(auto_attribs=True)
class NotificationCount:
    """ Notification schema for notification count. """

    n_unseen: int
    n_seen: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        n_unseen = self.n_unseen
        n_seen = self.n_seen

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "n_unseen": n_unseen,
            }
        )
        if n_seen is not UNSET:
            field_dict["n_seen"] = n_seen

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        n_unseen = d.pop("n_unseen")

        n_seen = d.pop("n_seen", UNSET)

        notification_count = cls(
            n_unseen=n_unseen,
            n_seen=n_seen,
        )

        notification_count.additional_properties = d
        return notification_count

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
