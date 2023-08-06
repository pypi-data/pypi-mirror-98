import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.block_from_digester import BlockFromDigester
from ..models.chunk_out_coordinates import ChunkOutCoordinates
from ..models.chunk_out_div_idxs import ChunkOutDivIdxs
from ..models.chunk_out_metadata import ChunkOutMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChunkOut")


@attr.s(auto_attribs=True)
class ChunkOut:
    """ Chunk return schema. """

    div_idxs: ChunkOutDivIdxs
    text: str
    pages: List[int]
    name: str
    display_name: str
    folder_id: int
    item_id: int
    extension: str
    is_current_version: bool
    size: int
    ocr: bool
    id: str
    version_id: int
    tag_names: Union[Unset, List[str]] = UNSET
    blocks: Union[Unset, List[BlockFromDigester]] = UNSET
    coordinates: Union[ChunkOutCoordinates, Unset] = UNSET
    language: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    metadata: Union[ChunkOutMetadata, Unset] = UNSET
    num_pages: Union[Unset, int] = UNSET
    created_on: Union[Unset, datetime.datetime] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET
    embedding: Union[Unset, List[float]] = UNSET
    is_semantic: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        div_idxs = self.div_idxs.to_dict()

        text = self.text
        pages = self.pages

        name = self.name
        display_name = self.display_name
        folder_id = self.folder_id
        item_id = self.item_id
        extension = self.extension
        is_current_version = self.is_current_version
        size = self.size
        ocr = self.ocr
        id = self.id
        version_id = self.version_id
        tag_names: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.tag_names, Unset):
            tag_names = self.tag_names

        blocks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.blocks, Unset):
            blocks = []
            for blocks_item_data in self.blocks:
                blocks_item = blocks_item_data.to_dict()

                blocks.append(blocks_item)

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        language = self.language
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

        embedding: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.embedding, Unset):
            embedding = self.embedding

        is_semantic = self.is_semantic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "div_idxs": div_idxs,
                "text": text,
                "pages": pages,
                "name": name,
                "display_name": display_name,
                "folder_id": folder_id,
                "item_id": item_id,
                "extension": extension,
                "is_current_version": is_current_version,
                "size": size,
                "ocr": ocr,
                "id": id,
                "version_id": version_id,
            }
        )
        if tag_names is not UNSET:
            field_dict["tag_names"] = tag_names
        if blocks is not UNSET:
            field_dict["blocks"] = blocks
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if language is not UNSET:
            field_dict["language"] = language
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
        if embedding is not UNSET:
            field_dict["embedding"] = embedding
        if is_semantic is not UNSET:
            field_dict["is_semantic"] = is_semantic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        div_idxs = ChunkOutDivIdxs.from_dict(d.pop("div_idxs"))

        text = d.pop("text")

        pages = cast(List[int], d.pop("pages"))

        name = d.pop("name")

        display_name = d.pop("display_name")

        folder_id = d.pop("folder_id")

        item_id = d.pop("item_id")

        extension = d.pop("extension")

        is_current_version = d.pop("is_current_version")

        size = d.pop("size")

        ocr = d.pop("ocr")

        id = d.pop("id")

        version_id = d.pop("version_id")

        tag_names = cast(List[str], d.pop("tag_names", UNSET))

        blocks = []
        _blocks = d.pop("blocks", UNSET)
        for blocks_item_data in _blocks or []:
            blocks_item = BlockFromDigester.from_dict(blocks_item_data)

            blocks.append(blocks_item)

        coordinates: Union[ChunkOutCoordinates, Unset] = UNSET
        _coordinates = d.pop("coordinates", UNSET)
        if not isinstance(_coordinates, Unset):
            coordinates = ChunkOutCoordinates.from_dict(_coordinates)

        language = d.pop("language", UNSET)

        title = d.pop("title", UNSET)

        author = d.pop("author", UNSET)

        metadata: Union[ChunkOutMetadata, Unset] = UNSET
        _metadata = d.pop("metadata", UNSET)
        if not isinstance(_metadata, Unset):
            metadata = ChunkOutMetadata.from_dict(_metadata)

        num_pages = d.pop("num_pages", UNSET)

        created_on: Union[Unset, datetime.datetime] = UNSET
        _created_on = d.pop("created_on", UNSET)
        if not isinstance(_created_on, Unset):
            created_on = isoparse(_created_on)

        updated_on: Union[Unset, datetime.datetime] = UNSET
        _updated_on = d.pop("updated_on", UNSET)
        if not isinstance(_updated_on, Unset):
            updated_on = isoparse(_updated_on)

        embedding = cast(List[float], d.pop("embedding", UNSET))

        is_semantic = d.pop("is_semantic", UNSET)

        chunk_out = cls(
            div_idxs=div_idxs,
            text=text,
            pages=pages,
            name=name,
            display_name=display_name,
            folder_id=folder_id,
            item_id=item_id,
            extension=extension,
            is_current_version=is_current_version,
            size=size,
            ocr=ocr,
            id=id,
            version_id=version_id,
            tag_names=tag_names,
            blocks=blocks,
            coordinates=coordinates,
            language=language,
            title=title,
            author=author,
            metadata=metadata,
            num_pages=num_pages,
            created_on=created_on,
            updated_on=updated_on,
            embedding=embedding,
            is_semantic=is_semantic,
        )

        chunk_out.additional_properties = d
        return chunk_out

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
