from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extract_top_chunk_validate_out_coordinates import ExtractTopChunkValidateOutCoordinates
from ..models.extract_top_chunk_validate_out_div_idxs import ExtractTopChunkValidateOutDivIdxs
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractTopChunkValidateOut")


@attr.s(auto_attribs=True)
class ExtractTopChunkValidateOut:
    """ Top chunk schema in extract result to validate. """

    result_id: int
    rank: int
    chunk_id: str
    page: int
    text: str
    div_idxs: Union[ExtractTopChunkValidateOutDivIdxs, Unset] = UNSET
    coordinates: Union[ExtractTopChunkValidateOutCoordinates, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result_id = self.result_id
        rank = self.rank
        chunk_id = self.chunk_id
        page = self.page
        text = self.text
        div_idxs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.div_idxs, Unset):
            div_idxs = self.div_idxs.to_dict()

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result_id": result_id,
                "rank": rank,
                "chunk_id": chunk_id,
                "page": page,
                "text": text,
            }
        )
        if div_idxs is not UNSET:
            field_dict["div_idxs"] = div_idxs
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result_id = d.pop("result_id")

        rank = d.pop("rank")

        chunk_id = d.pop("chunk_id")

        page = d.pop("page")

        text = d.pop("text")

        div_idxs: Union[ExtractTopChunkValidateOutDivIdxs, Unset] = UNSET
        _div_idxs = d.pop("div_idxs", UNSET)
        if not isinstance(_div_idxs, Unset):
            div_idxs = ExtractTopChunkValidateOutDivIdxs.from_dict(_div_idxs)

        coordinates: Union[ExtractTopChunkValidateOutCoordinates, Unset] = UNSET
        _coordinates = d.pop("coordinates", UNSET)
        if not isinstance(_coordinates, Unset):
            coordinates = ExtractTopChunkValidateOutCoordinates.from_dict(_coordinates)

        extract_top_chunk_validate_out = cls(
            result_id=result_id,
            rank=rank,
            chunk_id=chunk_id,
            page=page,
            text=text,
            div_idxs=div_idxs,
            coordinates=coordinates,
        )

        extract_top_chunk_validate_out.additional_properties = d
        return extract_top_chunk_validate_out

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
