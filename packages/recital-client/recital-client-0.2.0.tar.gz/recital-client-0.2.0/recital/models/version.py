import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.version_metadata import VersionMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="Version")


@attr.s(auto_attribs=True)
class Version:
    """ File Version schema. """

    id: int
    org_id: int
    folder_id: int
    item_id: int
    name: str
    display_name: str
    size: int
    extension: str
    is_current_version: bool
    title: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    language: Union[Unset, str] = UNSET
    num_pages: Union[Unset, int] = UNSET
    metadata: Union[VersionMetadata, Unset] = UNSET
    chunked: Union[Unset, bool] = False
    chunk_timestamp: Union[Unset, datetime.datetime] = UNSET
    ocr: Union[Unset, bool] = False
    created_on: Union[Unset, datetime.datetime] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET
    idx_task_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        org_id = self.org_id
        folder_id = self.folder_id
        item_id = self.item_id
        name = self.name
        display_name = self.display_name
        size = self.size
        extension = self.extension
        is_current_version = self.is_current_version
        title = self.title
        text = self.text
        author = self.author
        language = self.language
        num_pages = self.num_pages
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        chunked = self.chunked
        chunk_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.chunk_timestamp, Unset):
            chunk_timestamp = self.chunk_timestamp.isoformat()

        ocr = self.ocr
        created_on: Union[Unset, str] = UNSET
        if not isinstance(self.created_on, Unset):
            created_on = self.created_on.isoformat()

        updated_on: Union[Unset, str] = UNSET
        if not isinstance(self.updated_on, Unset):
            updated_on = self.updated_on.isoformat()

        idx_task_id = self.idx_task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "folder_id": folder_id,
                "item_id": item_id,
                "name": name,
                "display_name": display_name,
                "size": size,
                "extension": extension,
                "is_current_version": is_current_version,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if text is not UNSET:
            field_dict["text"] = text
        if author is not UNSET:
            field_dict["author"] = author
        if language is not UNSET:
            field_dict["language"] = language
        if num_pages is not UNSET:
            field_dict["num_pages"] = num_pages
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if chunked is not UNSET:
            field_dict["chunked"] = chunked
        if chunk_timestamp is not UNSET:
            field_dict["chunk_timestamp"] = chunk_timestamp
        if ocr is not UNSET:
            field_dict["ocr"] = ocr
        if created_on is not UNSET:
            field_dict["created_on"] = created_on
        if updated_on is not UNSET:
            field_dict["updated_on"] = updated_on
        if idx_task_id is not UNSET:
            field_dict["idx_task_id"] = idx_task_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        org_id = d.pop("org_id")

        folder_id = d.pop("folder_id")

        item_id = d.pop("item_id")

        name = d.pop("name")

        display_name = d.pop("display_name")

        size = d.pop("size")

        extension = d.pop("extension")

        is_current_version = d.pop("is_current_version")

        title = d.pop("title", UNSET)

        text = d.pop("text", UNSET)

        author = d.pop("author", UNSET)

        language = d.pop("language", UNSET)

        num_pages = d.pop("num_pages", UNSET)

        metadata: Union[VersionMetadata, Unset] = UNSET
        _metadata = d.pop("metadata", UNSET)
        if not isinstance(_metadata, Unset):
            metadata = VersionMetadata.from_dict(_metadata)

        chunked = d.pop("chunked", UNSET)

        chunk_timestamp: Union[Unset, datetime.datetime] = UNSET
        _chunk_timestamp = d.pop("chunk_timestamp", UNSET)
        if not isinstance(_chunk_timestamp, Unset):
            chunk_timestamp = isoparse(_chunk_timestamp)

        ocr = d.pop("ocr", UNSET)

        created_on: Union[Unset, datetime.datetime] = UNSET
        _created_on = d.pop("created_on", UNSET)
        if not isinstance(_created_on, Unset):
            created_on = isoparse(_created_on)

        updated_on: Union[Unset, datetime.datetime] = UNSET
        _updated_on = d.pop("updated_on", UNSET)
        if not isinstance(_updated_on, Unset):
            updated_on = isoparse(_updated_on)

        idx_task_id = d.pop("idx_task_id", UNSET)

        version = cls(
            id=id,
            org_id=org_id,
            folder_id=folder_id,
            item_id=item_id,
            name=name,
            display_name=display_name,
            size=size,
            extension=extension,
            is_current_version=is_current_version,
            title=title,
            text=text,
            author=author,
            language=language,
            num_pages=num_pages,
            metadata=metadata,
            chunked=chunked,
            chunk_timestamp=chunk_timestamp,
            ocr=ocr,
            created_on=created_on,
            updated_on=updated_on,
            idx_task_id=idx_task_id,
        )

        version.additional_properties = d
        return version

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
