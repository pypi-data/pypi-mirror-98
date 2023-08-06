from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PermissionUpdate")


@attr.s(auto_attribs=True)
class PermissionUpdate:
    """ Permission schema to receive from PUT method. """

    role: str
    product: str
    license_type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role
        product = self.product
        license_type = self.license_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "product": product,
                "license_type": license_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = d.pop("role")

        product = d.pop("product")

        license_type = d.pop("license_type")

        permission_update = cls(
            role=role,
            product=product,
            license_type=license_type,
        )

        permission_update.additional_properties = d
        return permission_update

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
