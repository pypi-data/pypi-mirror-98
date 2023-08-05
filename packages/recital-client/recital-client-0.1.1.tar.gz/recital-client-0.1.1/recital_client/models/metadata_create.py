from typing import Any, Dict, List, Union, cast

import attr

from ..models.metadata_date_range import MetadataDateRange
from ..models.metadata_type import MetadataType
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class MetadataCreate:
    """ Metadata schema for metadata creation. """

    name: str
    value_type: Union[Unset, MetadataType] = UNSET
    value: Union[Unset, MetadataDateRange, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value_type: Union[Unset, MetadataType] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type

        value: Union[Unset, MetadataDateRange, str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, MetadataDateRange):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value.to_dict()

        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if value_type is not UNSET:
            field_dict["value_type"] = value_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "MetadataCreate":
        d = src_dict.copy()
        name = d.pop("name")

        value_type = None
        _value_type = d.pop("value_type", UNSET)
        if _value_type is not None:
            value_type = MetadataType(_value_type)

        def _parse_value(data: Any) -> Union[Unset, MetadataDateRange, str]:
            data = None if isinstance(data, Unset) else data
            value: Union[Unset, MetadataDateRange, str]
            try:
                value = UNSET
                _value = data
                if _value is not None and not isinstance(_value, Unset):
                    value = MetadataDateRange.from_dict(cast(Dict[str, Any], _value))

                return value
            except:  # noqa: E722
                pass
            return d.pop("value", UNSET)

        value = _parse_value(d.pop("value", UNSET))

        metadata_create = MetadataCreate(
            name=name,
            value_type=value_type,
            value=value,
        )

        metadata_create.additional_properties = d
        return metadata_create

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
