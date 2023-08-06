from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ChunkBookmarkCreate")


@attr.s(auto_attribs=True)
class ChunkBookmarkCreate:
    """ Chunk bookmark schema to receive from the POST method. """

    query_id: int
    collection_id: int
    version_id: int
    chunk_id: str
    chunk_text: str
    from_semantic: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_id = self.query_id
        collection_id = self.collection_id
        version_id = self.version_id
        chunk_id = self.chunk_id
        chunk_text = self.chunk_text
        from_semantic = self.from_semantic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_id": query_id,
                "collection_id": collection_id,
                "version_id": version_id,
                "chunk_id": chunk_id,
                "chunk_text": chunk_text,
                "from_semantic": from_semantic,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_id = d.pop("query_id")

        collection_id = d.pop("collection_id")

        version_id = d.pop("version_id")

        chunk_id = d.pop("chunk_id")

        chunk_text = d.pop("chunk_text")

        from_semantic = d.pop("from_semantic")

        chunk_bookmark_create = cls(
            query_id=query_id,
            collection_id=collection_id,
            version_id=version_id,
            chunk_id=chunk_id,
            chunk_text=chunk_text,
            from_semantic=from_semantic,
        )

        chunk_bookmark_create.additional_properties = d
        return chunk_bookmark_create

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
