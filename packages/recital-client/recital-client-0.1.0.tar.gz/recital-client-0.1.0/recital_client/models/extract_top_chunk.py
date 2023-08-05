from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ExtractTopChunk:
    """ Top chunk schema to be returned from the API. """

    rank: int
    chunk_id: str
    page: int
    text: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rank = self.rank
        chunk_id = self.chunk_id
        page = self.page
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rank": rank,
                "chunk_id": chunk_id,
                "page": page,
                "text": text,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ExtractTopChunk":
        d = src_dict.copy()
        rank = d.pop("rank")

        chunk_id = d.pop("chunk_id")

        page = d.pop("page")

        text = d.pop("text")

        extract_top_chunk = ExtractTopChunk(
            rank=rank,
            chunk_id=chunk_id,
            page=page,
            text=text,
        )

        extract_top_chunk.additional_properties = d
        return extract_top_chunk

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
