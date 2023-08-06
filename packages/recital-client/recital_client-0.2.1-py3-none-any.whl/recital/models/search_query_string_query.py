from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.search_query_string_query_filters import SearchQueryStringQueryFilters
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchQueryStringQuery")


@attr.s(auto_attribs=True)
class SearchQueryStringQuery:
    """ Schema for string query search queries. """

    keywords: List[str]
    folder_ids: Union[Unset, List[int]] = UNSET
    output_fields: Union[Unset, List[str]] = UNSET
    filters: Union[SearchQueryStringQueryFilters, Unset] = UNSET
    keyword_op: Union[Unset, None] = UNSET
    file_ids: Union[Unset, List[int]] = UNSET
    query: Union[Unset, str] = UNSET
    keywords_only_query: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keywords = self.keywords

        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        output_fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.output_fields, Unset):
            output_fields = self.output_fields

        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        keyword_op = None

        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        query = self.query
        keywords_only_query = self.keywords_only_query

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keywords": keywords,
            }
        )
        if folder_ids is not UNSET:
            field_dict["folder_ids"] = folder_ids
        if output_fields is not UNSET:
            field_dict["output_fields"] = output_fields
        if filters is not UNSET:
            field_dict["filters"] = filters
        if keyword_op is not UNSET:
            field_dict["keyword_op"] = keyword_op
        if file_ids is not UNSET:
            field_dict["file_ids"] = file_ids
        if query is not UNSET:
            field_dict["query"] = query
        if keywords_only_query is not UNSET:
            field_dict["keywords_only_query"] = keywords_only_query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        keywords = cast(List[str], d.pop("keywords"))

        folder_ids = cast(List[int], d.pop("folder_ids", UNSET))

        output_fields = cast(List[str], d.pop("output_fields", UNSET))

        filters: Union[SearchQueryStringQueryFilters, Unset] = UNSET
        _filters = d.pop("filters", UNSET)
        if not isinstance(_filters, Unset):
            filters = SearchQueryStringQueryFilters.from_dict(_filters)

        keyword_op = None

        file_ids = cast(List[int], d.pop("file_ids", UNSET))

        query = d.pop("query", UNSET)

        keywords_only_query = d.pop("keywords_only_query", UNSET)

        search_query_string_query = cls(
            keywords=keywords,
            folder_ids=folder_ids,
            output_fields=output_fields,
            filters=filters,
            keyword_op=keyword_op,
            file_ids=file_ids,
            query=query,
            keywords_only_query=keywords_only_query,
        )

        search_query_string_query.additional_properties = d
        return search_query_string_query

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
