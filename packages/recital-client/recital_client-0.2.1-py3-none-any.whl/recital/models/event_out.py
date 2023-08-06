import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.event_out_args import EventOutArgs

T = TypeVar("T", bound="EventOut")


@attr.s(auto_attribs=True)
class EventOut:
    """ Event schema to output from GET methods. """

    user_name: str
    timestamp: datetime.datetime
    code: int
    desc: str
    args: EventOutArgs
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_name = self.user_name
        timestamp = self.timestamp.isoformat()

        code = self.code
        desc = self.desc
        args = self.args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_name": user_name,
                "timestamp": timestamp,
                "code": code,
                "desc": desc,
                "args": args,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_name = d.pop("user_name")

        timestamp = isoparse(d.pop("timestamp"))

        code = d.pop("code")

        desc = d.pop("desc")

        args = EventOutArgs.from_dict(d.pop("args"))

        event_out = cls(
            user_name=user_name,
            timestamp=timestamp,
            code=code,
            desc=desc,
            args=args,
        )

        event_out.additional_properties = d
        return event_out

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
