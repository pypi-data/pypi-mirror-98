from typing import Any, Dict, List, Union, cast

import attr

from ..models.search_query_string_query_filters import SearchQueryStringQueryFilters
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SearchQueryStringQuery:
    """ Schema for string query search queries. """

    keywords: List[str]
    query: str
    folder_ids: Union[Unset, List[int]] = UNSET
    filters: Union[SearchQueryStringQueryFilters, Unset] = UNSET
    keyword_op: Union[Unset, None] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keywords = self.keywords

        query = self.query
        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        keyword_op = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keywords": keywords,
                "query": query,
            }
        )
        if folder_ids is not UNSET:
            field_dict["folder_ids"] = folder_ids
        if filters is not UNSET:
            field_dict["filters"] = filters
        if keyword_op is not UNSET:
            field_dict["keyword_op"] = keyword_op

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SearchQueryStringQuery":
        d = src_dict.copy()
        keywords = cast(List[str], d.pop("keywords"))

        query = d.pop("query")

        folder_ids = cast(List[int], d.pop("folder_ids", UNSET))

        filters: Union[SearchQueryStringQueryFilters, Unset] = UNSET
        _filters = d.pop("filters", UNSET)
        if _filters is not None and not isinstance(_filters, Unset):
            filters = SearchQueryStringQueryFilters.from_dict(cast(Dict[str, Any], _filters))

        keyword_op = None

        search_query_string_query = SearchQueryStringQuery(
            keywords=keywords,
            query=query,
            folder_ids=folder_ids,
            filters=filters,
            keyword_op=keyword_op,
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
