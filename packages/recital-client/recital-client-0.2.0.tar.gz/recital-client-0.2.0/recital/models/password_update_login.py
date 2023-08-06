from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PasswordUpdateLogin")


@attr.s(auto_attribs=True)
class PasswordUpdateLogin:
    """ Password Update data used as input in the POST /{user_email}/password_recovery_confirm endpoint. """

    new_password: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_password = self.new_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_password": new_password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_password = d.pop("new_password")

        password_update_login = cls(
            new_password=new_password,
        )

        password_update_login.additional_properties = d
        return password_update_login

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
