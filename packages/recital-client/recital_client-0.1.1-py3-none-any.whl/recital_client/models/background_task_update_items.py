from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class BackgroundTaskUpdateItems:
    """Background task schema for updating
    number of processed items in a task."""

    items: int
    time: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items = self.items
        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "time": time,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BackgroundTaskUpdateItems":
        d = src_dict.copy()
        items = d.pop("items")

        time = d.pop("time")

        background_task_update_items = BackgroundTaskUpdateItems(
            items=items,
            time=time,
        )

        background_task_update_items.additional_properties = d
        return background_task_update_items

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
