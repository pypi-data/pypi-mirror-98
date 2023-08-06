from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.chunk_bookmark_out import ChunkBookmarkOut

T = TypeVar("T", bound="ChunkBookmarkResult")


@attr.s(auto_attribs=True)
class ChunkBookmarkResult:
    """ Chunk bookmark result schema. """

    chunks: List[ChunkBookmarkOut]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chunks = []
        for chunks_item_data in self.chunks:
            chunks_item = chunks_item_data.to_dict()

            chunks.append(chunks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chunks": chunks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chunks = []
        _chunks = d.pop("chunks")
        for chunks_item_data in _chunks:
            chunks_item = ChunkBookmarkOut.from_dict(chunks_item_data)

            chunks.append(chunks_item)

        chunk_bookmark_result = cls(
            chunks=chunks,
        )

        chunk_bookmark_result.additional_properties = d
        return chunk_bookmark_result

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
