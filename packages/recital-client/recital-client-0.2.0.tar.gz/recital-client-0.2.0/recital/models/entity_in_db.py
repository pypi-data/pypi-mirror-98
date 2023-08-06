from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntityInDB")


@attr.s(auto_attribs=True)
class EntityInDB:
    """ Document entity schema. """

    chunk_id: str
    type: str
    text: str
    id: int
    version_id: int
    page_start: int
    page_end: int
    div_start: Union[Unset, int] = UNSET
    starts_at: Union[Unset, int] = UNSET
    div_end: Union[Unset, int] = UNSET
    ends_at: Union[Unset, int] = UNSET
    score: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chunk_id = self.chunk_id
        type = self.type
        text = self.text
        id = self.id
        version_id = self.version_id
        page_start = self.page_start
        page_end = self.page_end
        div_start = self.div_start
        starts_at = self.starts_at
        div_end = self.div_end
        ends_at = self.ends_at
        score = self.score

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chunk_id": chunk_id,
                "type": type,
                "text": text,
                "id": id,
                "version_id": version_id,
                "page_start": page_start,
                "page_end": page_end,
            }
        )
        if div_start is not UNSET:
            field_dict["div_start"] = div_start
        if starts_at is not UNSET:
            field_dict["starts_at"] = starts_at
        if div_end is not UNSET:
            field_dict["div_end"] = div_end
        if ends_at is not UNSET:
            field_dict["ends_at"] = ends_at
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chunk_id = d.pop("chunk_id")

        type = d.pop("type")

        text = d.pop("text")

        id = d.pop("id")

        version_id = d.pop("version_id")

        page_start = d.pop("page_start")

        page_end = d.pop("page_end")

        div_start = d.pop("div_start", UNSET)

        starts_at = d.pop("starts_at", UNSET)

        div_end = d.pop("div_end", UNSET)

        ends_at = d.pop("ends_at", UNSET)

        score = d.pop("score", UNSET)

        entity_in_db = cls(
            chunk_id=chunk_id,
            type=type,
            text=text,
            id=id,
            version_id=version_id,
            page_start=page_start,
            page_end=page_end,
            div_start=div_start,
            starts_at=starts_at,
            div_end=div_end,
            ends_at=ends_at,
            score=score,
        )

        entity_in_db.additional_properties = d
        return entity_in_db

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
