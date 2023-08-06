import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.extract_top_chunk import ExtractTopChunk

T = TypeVar("T", bound="ExtractPredictionIn")


@attr.s(auto_attribs=True)
class ExtractPredictionIn:
    """ Schema for POST /predictions. """

    batch_processed_at: datetime.datetime
    top_chunks: List[ExtractTopChunk]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch_processed_at = self.batch_processed_at.isoformat()

        top_chunks = []
        for top_chunks_item_data in self.top_chunks:
            top_chunks_item = top_chunks_item_data.to_dict()

            top_chunks.append(top_chunks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batch_processed_at": batch_processed_at,
                "top_chunks": top_chunks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_processed_at = isoparse(d.pop("batch_processed_at"))

        top_chunks = []
        _top_chunks = d.pop("top_chunks")
        for top_chunks_item_data in _top_chunks:
            top_chunks_item = ExtractTopChunk.from_dict(top_chunks_item_data)

            top_chunks.append(top_chunks_item)

        extract_prediction_in = cls(
            batch_processed_at=batch_processed_at,
            top_chunks=top_chunks,
        )

        extract_prediction_in.additional_properties = d
        return extract_prediction_in

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
