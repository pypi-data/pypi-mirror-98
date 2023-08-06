import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.product import Product
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationUpdate")


@attr.s(auto_attribs=True)
class OrganizationUpdate:
    """ Organization schema to receive from PUT method. """

    name: Union[Unset, str] = UNSET
    product: Union[Unset, Product] = UNSET
    license_expires_on: Union[Unset, datetime.datetime] = UNSET
    license_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        product: Union[Unset, Product] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product

        license_expires_on: Union[Unset, str] = UNSET
        if not isinstance(self.license_expires_on, Unset):
            license_expires_on = self.license_expires_on.isoformat()

        license_type = self.license_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if product is not UNSET:
            field_dict["product"] = product
        if license_expires_on is not UNSET:
            field_dict["license_expires_on"] = license_expires_on
        if license_type is not UNSET:
            field_dict["license_type"] = license_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        product: Union[Unset, Product] = UNSET
        _product = d.pop("product", UNSET)
        if not isinstance(_product, Unset):
            product = Product(_product)

        license_expires_on: Union[Unset, datetime.datetime] = UNSET
        _license_expires_on = d.pop("license_expires_on", UNSET)
        if not isinstance(_license_expires_on, Unset):
            license_expires_on = isoparse(_license_expires_on)

        license_type = d.pop("license_type", UNSET)

        organization_update = cls(
            name=name,
            product=product,
            license_expires_on=license_expires_on,
            license_type=license_type,
        )

        organization_update.additional_properties = d
        return organization_update

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
