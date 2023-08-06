from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.document_outline_out_outline_item import DocumentOutlineOutOutlineItem

T = TypeVar("T", bound="DocumentOutlineOut")


@attr.s(auto_attribs=True)
class DocumentOutlineOut:
    """ Document Outline schema for database input """

    outline: List[DocumentOutlineOutOutlineItem]
    version_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        outline = []
        for outline_item_data in self.outline:
            outline_item = outline_item_data.to_dict()

            outline.append(outline_item)

        version_id = self.version_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "outline": outline,
                "version_id": version_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        outline = []
        _outline = d.pop("outline")
        for outline_item_data in _outline:
            outline_item = DocumentOutlineOutOutlineItem.from_dict(outline_item_data)

            outline.append(outline_item)

        version_id = d.pop("version_id")

        document_outline_out = cls(
            outline=outline,
            version_id=version_id,
        )

        document_outline_out.additional_properties = d
        return document_outline_out

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
