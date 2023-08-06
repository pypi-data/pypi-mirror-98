import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.document_result_metadata import DocumentResultMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentResult")


@attr.s(auto_attribs=True)
class DocumentResult:
    """ Document result schema. """

    name: str
    display_name: str
    folder_id: int
    item_id: int
    extension: str
    is_current_version: bool
    size: int
    ocr: bool
    id: int
    title: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    metadata: Union[DocumentResultMetadata, Unset] = UNSET
    num_pages: Union[Unset, int] = UNSET
    created_on: Union[Unset, datetime.datetime] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        display_name = self.display_name
        folder_id = self.folder_id
        item_id = self.item_id
        extension = self.extension
        is_current_version = self.is_current_version
        size = self.size
        ocr = self.ocr
        id = self.id
        title = self.title
        author = self.author
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        num_pages = self.num_pages
        created_on: Union[Unset, str] = UNSET
        if not isinstance(self.created_on, Unset):
            created_on = self.created_on.isoformat()

        updated_on: Union[Unset, str] = UNSET
        if not isinstance(self.updated_on, Unset):
            updated_on = self.updated_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "display_name": display_name,
                "folder_id": folder_id,
                "item_id": item_id,
                "extension": extension,
                "is_current_version": is_current_version,
                "size": size,
                "ocr": ocr,
                "id": id,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if author is not UNSET:
            field_dict["author"] = author
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if num_pages is not UNSET:
            field_dict["num_pages"] = num_pages
        if created_on is not UNSET:
            field_dict["created_on"] = created_on
        if updated_on is not UNSET:
            field_dict["updated_on"] = updated_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        display_name = d.pop("display_name")

        folder_id = d.pop("folder_id")

        item_id = d.pop("item_id")

        extension = d.pop("extension")

        is_current_version = d.pop("is_current_version")

        size = d.pop("size")

        ocr = d.pop("ocr")

        id = d.pop("id")

        title = d.pop("title", UNSET)

        author = d.pop("author", UNSET)

        metadata: Union[DocumentResultMetadata, Unset] = UNSET
        _metadata = d.pop("metadata", UNSET)
        if not isinstance(_metadata, Unset):
            metadata = DocumentResultMetadata.from_dict(_metadata)

        num_pages = d.pop("num_pages", UNSET)

        created_on: Union[Unset, datetime.datetime] = UNSET
        _created_on = d.pop("created_on", UNSET)
        if not isinstance(_created_on, Unset):
            created_on = isoparse(_created_on)

        updated_on: Union[Unset, datetime.datetime] = UNSET
        _updated_on = d.pop("updated_on", UNSET)
        if not isinstance(_updated_on, Unset):
            updated_on = isoparse(_updated_on)

        document_result = cls(
            name=name,
            display_name=display_name,
            folder_id=folder_id,
            item_id=item_id,
            extension=extension,
            is_current_version=is_current_version,
            size=size,
            ocr=ocr,
            id=id,
            title=title,
            author=author,
            metadata=metadata,
            num_pages=num_pages,
            created_on=created_on,
            updated_on=updated_on,
        )

        document_result.additional_properties = d
        return document_result

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
