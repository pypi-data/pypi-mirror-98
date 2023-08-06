from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.source_filters import SourceFilters
from ..models.source_type import SourceType

T = TypeVar("T", bound="DocSource")


@attr.s(auto_attribs=True)
class DocSource:
    """ Document source schema. """

    source_type: SourceType
    source_filters: SourceFilters
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_type = self.source_type.value

        source_filters = self.source_filters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_type": source_type,
                "source_filters": source_filters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_type = SourceType(d.pop("source_type"))

        source_filters = SourceFilters.from_dict(d.pop("source_filters"))

        doc_source = cls(
            source_type=source_type,
            source_filters=source_filters,
        )

        doc_source.additional_properties = d
        return doc_source

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
