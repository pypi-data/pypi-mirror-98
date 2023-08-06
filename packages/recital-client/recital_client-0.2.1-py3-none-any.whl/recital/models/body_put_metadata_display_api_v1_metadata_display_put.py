from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="BodyPutMetadataDisplayApiV1MetadataDisplay_Put")


@attr.s(auto_attribs=True)
class BodyPutMetadataDisplayApiV1MetadataDisplay_Put:
    """  """

    primary_filters: List[int]
    secondary_filters: List[int]
    chunks_results: List[int]
    sorting_metadata: List[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        primary_filters = self.primary_filters

        secondary_filters = self.secondary_filters

        chunks_results = self.chunks_results

        sorting_metadata = self.sorting_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "primary_filters": primary_filters,
                "secondary_filters": secondary_filters,
                "chunks_results": chunks_results,
                "sorting_metadata": sorting_metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        primary_filters = cast(List[int], d.pop("primary_filters"))

        secondary_filters = cast(List[int], d.pop("secondary_filters"))

        chunks_results = cast(List[int], d.pop("chunks_results"))

        sorting_metadata = cast(List[int], d.pop("sorting_metadata"))

        body_put_metadata_display_api_v1_metadata_display_put = cls(
            primary_filters=primary_filters,
            secondary_filters=secondary_filters,
            chunks_results=chunks_results,
            sorting_metadata=sorting_metadata,
        )

        body_put_metadata_display_api_v1_metadata_display_put.additional_properties = d
        return body_put_metadata_display_api_v1_metadata_display_put

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
