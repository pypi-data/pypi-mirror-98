import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackgroundTaskOut")


@attr.s(auto_attribs=True)
class BackgroundTaskOut:
    """ Background task schema to output from GET methods. """

    user_id: int
    name: str
    task_type: str
    total_items: int
    id: int
    created_on: datetime.datetime
    processed_items: int
    total_time: float
    status: str
    done_on: Union[Unset, datetime.datetime] = UNSET
    link: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        name = self.name
        task_type = self.task_type
        total_items = self.total_items
        id = self.id
        created_on = self.created_on.isoformat()

        processed_items = self.processed_items
        total_time = self.total_time
        status = self.status
        done_on: Union[Unset, str] = UNSET
        if not isinstance(self.done_on, Unset):
            done_on = self.done_on.isoformat()

        link = self.link

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "name": name,
                "task_type": task_type,
                "total_items": total_items,
                "id": id,
                "created_on": created_on,
                "processed_items": processed_items,
                "total_time": total_time,
                "status": status,
            }
        )
        if done_on is not UNSET:
            field_dict["done_on"] = done_on
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id")

        name = d.pop("name")

        task_type = d.pop("task_type")

        total_items = d.pop("total_items")

        id = d.pop("id")

        created_on = isoparse(d.pop("created_on"))

        processed_items = d.pop("processed_items")

        total_time = d.pop("total_time")

        status = d.pop("status")

        done_on: Union[Unset, datetime.datetime] = UNSET
        _done_on = d.pop("done_on", UNSET)
        if not isinstance(_done_on, Unset):
            done_on = isoparse(_done_on)

        link = d.pop("link", UNSET)

        background_task_out = cls(
            user_id=user_id,
            name=name,
            task_type=task_type,
            total_items=total_items,
            id=id,
            created_on=created_on,
            processed_items=processed_items,
            total_time=total_time,
            status=status,
            done_on=done_on,
            link=link,
        )

        background_task_out.additional_properties = d
        return background_task_out

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
