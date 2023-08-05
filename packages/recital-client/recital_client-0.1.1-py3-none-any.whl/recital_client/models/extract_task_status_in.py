from typing import Any, Dict, List

import attr

from ..models.extract_task_status import ExtractTaskStatus


@attr.s(auto_attribs=True)
class ExtractTaskStatusIn:
    """ Extract task status model for updates """

    status: ExtractTaskStatus
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ExtractTaskStatusIn":
        d = src_dict.copy()
        status = ExtractTaskStatus(d.pop("status"))

        extract_task_status_in = ExtractTaskStatusIn(
            status=status,
        )

        extract_task_status_in.additional_properties = d
        return extract_task_status_in

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
