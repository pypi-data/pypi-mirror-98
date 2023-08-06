from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackgroundTaskIn")


@attr.s(auto_attribs=True)
class BackgroundTaskIn:
    """ Background task schema for the POST route. """

    name: str
    task_type: str
    total_items: Union[Unset, int] = UNSET
    user_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        task_type = self.task_type
        total_items = self.total_items
        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "task_type": task_type,
            }
        )
        if total_items is not UNSET:
            field_dict["total_items"] = total_items
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        task_type = d.pop("task_type")

        total_items = d.pop("total_items", UNSET)

        user_id = d.pop("user_id", UNSET)

        background_task_in = cls(
            name=name,
            task_type=task_type,
            total_items=total_items,
            user_id=user_id,
        )

        background_task_in.additional_properties = d
        return background_task_in

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
