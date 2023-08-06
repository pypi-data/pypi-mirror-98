from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.search_query_keywords import SearchQueryKeywords

T = TypeVar("T", bound="DocSearchMetadataName")


@attr.s(auto_attribs=True)
class DocSearchMetadataName:
    """ Input schema for metadata count in document results. """

    query: SearchQueryKeywords
    metadata_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query.to_dict()

        metadata_name = self.metadata_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "metadata_name": metadata_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = SearchQueryKeywords.from_dict(d.pop("query"))

        metadata_name = d.pop("metadata_name")

        doc_search_metadata_name = cls(
            query=query,
            metadata_name=metadata_name,
        )

        doc_search_metadata_name.additional_properties = d
        return doc_search_metadata_name

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
