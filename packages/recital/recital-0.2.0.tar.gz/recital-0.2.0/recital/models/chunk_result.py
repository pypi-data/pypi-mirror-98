import datetime
from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.chunk_result_coordinates import ChunkResultCoordinates
from ..models.chunk_result_div_idxs import ChunkResultDivIdxs
from ..models.chunk_result_duplicates_item import ChunkResultDuplicatesItem
from ..models.chunk_result_metadata import ChunkResultMetadata
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="ChunkResult")


@attr.s(auto_attribs=True)
class ChunkResult:
    """ Chunk result schema. """

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
    div_idxs: ChunkResultDivIdxs
    pages: List[int]
    title: Union[Unset, str] = UNSET
    author: Union[Unset, str] = UNSET
    metadata: Union[ChunkResultMetadata, Unset] = UNSET
    num_pages: Union[Unset, int] = UNSET
    created_on: Union[Unset, datetime.datetime] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET
    text: Union[Unset, str] = UNSET
    image: Union[Unset, File] = UNSET
    coordinates: Union[ChunkResultCoordinates, Unset] = UNSET
    is_semantic: Union[Unset, bool] = False
    duplicates: Union[Unset, List[ChunkResultDuplicatesItem]] = UNSET
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
        version_id = self.version_id
        div_idxs = self.div_idxs.to_dict()

        pages = self.pages

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

        text = self.text
        image: Union[Unset, File] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_tuple()

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        is_semantic = self.is_semantic
        duplicates: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.duplicates, Unset):
            duplicates = []
            for duplicates_item_data in self.duplicates:
                duplicates_item = duplicates_item_data.to_dict()

                duplicates.append(duplicates_item)

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
                "version_id": version_id,
                "div_idxs": div_idxs,
                "pages": pages,
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
        if text is not UNSET:
            field_dict["text"] = text
        if image is not UNSET:
            field_dict["image"] = image
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if is_semantic is not UNSET:
            field_dict["is_semantic"] = is_semantic
        if duplicates is not UNSET:
            field_dict["duplicates"] = duplicates

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

        version_id = d.pop("version_id")

        div_idxs = ChunkResultDivIdxs.from_dict(d.pop("div_idxs"))

        pages = cast(List[int], d.pop("pages"))

        title = d.pop("title", UNSET)

        author = d.pop("author", UNSET)

        metadata: Union[ChunkResultMetadata, Unset] = UNSET
        _metadata = d.pop("metadata", UNSET)
        if not isinstance(_metadata, Unset):
            metadata = ChunkResultMetadata.from_dict(_metadata)

        num_pages = d.pop("num_pages", UNSET)

        created_on: Union[Unset, datetime.datetime] = UNSET
        _created_on = d.pop("created_on", UNSET)
        if not isinstance(_created_on, Unset):
            created_on = isoparse(_created_on)

        updated_on: Union[Unset, datetime.datetime] = UNSET
        _updated_on = d.pop("updated_on", UNSET)
        if not isinstance(_updated_on, Unset):
            updated_on = isoparse(_updated_on)

        text = d.pop("text", UNSET)

        image: Union[Unset, File] = UNSET
        _image = d.pop("image", UNSET)
        if not isinstance(_image, Unset):
            image = File(payload=BytesIO(_image))

        coordinates: Union[ChunkResultCoordinates, Unset] = UNSET
        _coordinates = d.pop("coordinates", UNSET)
        if not isinstance(_coordinates, Unset):
            coordinates = ChunkResultCoordinates.from_dict(_coordinates)

        is_semantic = d.pop("is_semantic", UNSET)

        duplicates = []
        _duplicates = d.pop("duplicates", UNSET)
        for duplicates_item_data in _duplicates or []:
            duplicates_item = ChunkResultDuplicatesItem.from_dict(duplicates_item_data)

            duplicates.append(duplicates_item)

        chunk_result = cls(
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
            div_idxs=div_idxs,
            pages=pages,
            title=title,
            author=author,
            metadata=metadata,
            num_pages=num_pages,
            created_on=created_on,
            updated_on=updated_on,
            text=text,
            image=image,
            coordinates=coordinates,
            is_semantic=is_semantic,
            duplicates=duplicates,
        )

        chunk_result.additional_properties = d
        return chunk_result

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
