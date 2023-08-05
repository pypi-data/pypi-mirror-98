from typing import Any, Dict, List

import attr

from ..models.search_query_keywords import SearchQueryKeywords


@attr.s(auto_attribs=True)
class DocSearchMetadata:
    """ Input schema for metadata assignment in document results. """

    query: SearchQueryKeywords
    metadata_name: str
    metadata_value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query.to_dict()

        metadata_name = self.metadata_name
        metadata_value = self.metadata_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "metadata_name": metadata_name,
                "metadata_value": metadata_value,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "DocSearchMetadata":
        d = src_dict.copy()
        query = SearchQueryKeywords.from_dict(d.pop("query"))

        metadata_name = d.pop("metadata_name")

        metadata_value = d.pop("metadata_value")

        doc_search_metadata = DocSearchMetadata(
            query=query,
            metadata_name=metadata_name,
            metadata_value=metadata_value,
        )

        doc_search_metadata.additional_properties = d
        return doc_search_metadata

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
