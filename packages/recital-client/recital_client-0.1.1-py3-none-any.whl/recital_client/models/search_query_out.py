import datetime
from typing import Any, Dict, List, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.search_query_out_filters import SearchQueryOutFilters
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SearchQueryOut:
    """ Search query schema to output from GET method. """

    user_id: int
    org_id: int
    queried_on: datetime.datetime
    id: int
    folder_ids: Union[Unset, List[int]] = UNSET
    filters: Union[SearchQueryOutFilters, Unset] = UNSET
    keywords: Union[Unset, List[str]] = UNSET
    keyword_op: Union[Unset, None] = UNSET
    query: Union[Unset, str] = UNSET
    is_doc_search: Union[Unset, bool] = False
    last_version: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        org_id = self.org_id
        queried_on = self.queried_on.isoformat()

        id = self.id
        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        keywords: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        keyword_op = None

        query = self.query
        is_doc_search = self.is_doc_search
        last_version = self.last_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "org_id": org_id,
                "queried_on": queried_on,
                "id": id,
            }
        )
        if folder_ids is not UNSET:
            field_dict["folder_ids"] = folder_ids
        if filters is not UNSET:
            field_dict["filters"] = filters
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if keyword_op is not UNSET:
            field_dict["keyword_op"] = keyword_op
        if query is not UNSET:
            field_dict["query"] = query
        if is_doc_search is not UNSET:
            field_dict["is_doc_search"] = is_doc_search
        if last_version is not UNSET:
            field_dict["last_version"] = last_version

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SearchQueryOut":
        d = src_dict.copy()
        user_id = d.pop("user_id")

        org_id = d.pop("org_id")

        queried_on = isoparse(d.pop("queried_on"))

        id = d.pop("id")

        folder_ids = cast(List[int], d.pop("folder_ids", UNSET))

        filters: Union[SearchQueryOutFilters, Unset] = UNSET
        _filters = d.pop("filters", UNSET)
        if _filters is not None and not isinstance(_filters, Unset):
            filters = SearchQueryOutFilters.from_dict(cast(Dict[str, Any], _filters))

        keywords = cast(List[str], d.pop("keywords", UNSET))

        keyword_op = None

        query = d.pop("query", UNSET)

        is_doc_search = d.pop("is_doc_search", UNSET)

        last_version = d.pop("last_version", UNSET)

        search_query_out = SearchQueryOut(
            user_id=user_id,
            org_id=org_id,
            queried_on=queried_on,
            id=id,
            folder_ids=folder_ids,
            filters=filters,
            keywords=keywords,
            keyword_op=keyword_op,
            query=query,
            is_doc_search=is_doc_search,
            last_version=last_version,
        )

        search_query_out.additional_properties = d
        return search_query_out

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
