import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.notification_out_args import NotificationOutArgs
from ..models.notification_out_info import NotificationOutInfo

T = TypeVar("T", bound="NotificationOut")


@attr.s(auto_attribs=True)
class NotificationOut:
    """ Notification schema to output from GET methods. """

    user_id: int
    message: str
    code: int
    args: NotificationOutArgs
    seen: bool
    info: NotificationOutInfo
    id: int
    timestamp: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        message = self.message
        code = self.code
        args = self.args.to_dict()

        seen = self.seen
        info = self.info.to_dict()

        id = self.id
        timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "message": message,
                "code": code,
                "args": args,
                "seen": seen,
                "info": info,
                "id": id,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id")

        message = d.pop("message")

        code = d.pop("code")

        args = NotificationOutArgs.from_dict(d.pop("args"))

        seen = d.pop("seen")

        info = NotificationOutInfo.from_dict(d.pop("info"))

        id = d.pop("id")

        timestamp = isoparse(d.pop("timestamp"))

        notification_out = cls(
            user_id=user_id,
            message=message,
            code=code,
            args=args,
            seen=seen,
            info=info,
            id=id,
            timestamp=timestamp,
        )

        notification_out.additional_properties = d
        return notification_out

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
