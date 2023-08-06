from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metadata_out import MetadataOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataDisplayOut")


@attr.s(auto_attribs=True)
class MetadataDisplayOut:
    """ Schema representing metadata display options to output in GET method. """

    primary_filters: Union[Unset, List[MetadataOut]] = UNSET
    secondary_filters: Union[Unset, List[MetadataOut]] = UNSET
    chunks_results: Union[Unset, List[MetadataOut]] = UNSET
    sorting_metadata: Union[Unset, List[MetadataOut]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        primary_filters: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.primary_filters, Unset):
            primary_filters = []
            for primary_filters_item_data in self.primary_filters:
                primary_filters_item = primary_filters_item_data.to_dict()

                primary_filters.append(primary_filters_item)

        secondary_filters: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.secondary_filters, Unset):
            secondary_filters = []
            for secondary_filters_item_data in self.secondary_filters:
                secondary_filters_item = secondary_filters_item_data.to_dict()

                secondary_filters.append(secondary_filters_item)

        chunks_results: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.chunks_results, Unset):
            chunks_results = []
            for chunks_results_item_data in self.chunks_results:
                chunks_results_item = chunks_results_item_data.to_dict()

                chunks_results.append(chunks_results_item)

        sorting_metadata: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sorting_metadata, Unset):
            sorting_metadata = []
            for sorting_metadata_item_data in self.sorting_metadata:
                sorting_metadata_item = sorting_metadata_item_data.to_dict()

                sorting_metadata.append(sorting_metadata_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if primary_filters is not UNSET:
            field_dict["primary_filters"] = primary_filters
        if secondary_filters is not UNSET:
            field_dict["secondary_filters"] = secondary_filters
        if chunks_results is not UNSET:
            field_dict["chunks_results"] = chunks_results
        if sorting_metadata is not UNSET:
            field_dict["sorting_metadata"] = sorting_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        primary_filters = []
        _primary_filters = d.pop("primary_filters", UNSET)
        for primary_filters_item_data in _primary_filters or []:
            primary_filters_item = MetadataOut.from_dict(primary_filters_item_data)

            primary_filters.append(primary_filters_item)

        secondary_filters = []
        _secondary_filters = d.pop("secondary_filters", UNSET)
        for secondary_filters_item_data in _secondary_filters or []:
            secondary_filters_item = MetadataOut.from_dict(secondary_filters_item_data)

            secondary_filters.append(secondary_filters_item)

        chunks_results = []
        _chunks_results = d.pop("chunks_results", UNSET)
        for chunks_results_item_data in _chunks_results or []:
            chunks_results_item = MetadataOut.from_dict(chunks_results_item_data)

            chunks_results.append(chunks_results_item)

        sorting_metadata = []
        _sorting_metadata = d.pop("sorting_metadata", UNSET)
        for sorting_metadata_item_data in _sorting_metadata or []:
            sorting_metadata_item = MetadataOut.from_dict(sorting_metadata_item_data)

            sorting_metadata.append(sorting_metadata_item)

        metadata_display_out = cls(
            primary_filters=primary_filters,
            secondary_filters=secondary_filters,
            chunks_results=chunks_results,
            sorting_metadata=sorting_metadata,
        )

        metadata_display_out.additional_properties = d
        return metadata_display_out

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
