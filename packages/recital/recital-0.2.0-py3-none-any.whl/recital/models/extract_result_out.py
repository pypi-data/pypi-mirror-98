import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.extract_result_out_metadata import ExtractResultOutMetadata
from ..models.extract_result_out_version_metadata import ExtractResultOutVersionMetadata
from ..models.extract_top_chunk_out import ExtractTopChunkOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractResultOut")


@attr.s(auto_attribs=True)
class ExtractResultOut:
    """ Extract result schema to be returned from the API. """

    task_id: int
    doc_id: int
    doc_filename: str
    doc_path: str
    id: int
    metadata: ExtractResultOutMetadata
    top_chunks: List[ExtractTopChunkOut]
    validated_by: Union[Unset, str] = UNSET
    validated_on: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, str] = UNSET
    found: Union[Unset, bool] = UNSET
    chunk_id: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    outdated: Union[Unset, bool] = UNSET
    version_metadata: Union[ExtractResultOutVersionMetadata, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id
        doc_id = self.doc_id
        doc_filename = self.doc_filename
        doc_path = self.doc_path
        id = self.id
        metadata = self.metadata.to_dict()

        top_chunks = []
        for top_chunks_item_data in self.top_chunks:
            top_chunks_item = top_chunks_item_data.to_dict()

            top_chunks.append(top_chunks_item)

        validated_by = self.validated_by
        validated_on: Union[Unset, str] = UNSET
        if not isinstance(self.validated_on, Unset):
            validated_on = self.validated_on.isoformat()

        status = self.status
        found = self.found
        chunk_id = self.chunk_id
        text = self.text
        outdated = self.outdated
        version_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.version_metadata, Unset):
            version_metadata = self.version_metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task_id": task_id,
                "doc_id": doc_id,
                "doc_filename": doc_filename,
                "doc_path": doc_path,
                "id": id,
                "metadata": metadata,
                "top_chunks": top_chunks,
            }
        )
        if validated_by is not UNSET:
            field_dict["validated_by"] = validated_by
        if validated_on is not UNSET:
            field_dict["validated_on"] = validated_on
        if status is not UNSET:
            field_dict["status"] = status
        if found is not UNSET:
            field_dict["found"] = found
        if chunk_id is not UNSET:
            field_dict["chunk_id"] = chunk_id
        if text is not UNSET:
            field_dict["text"] = text
        if outdated is not UNSET:
            field_dict["outdated"] = outdated
        if version_metadata is not UNSET:
            field_dict["version_metadata"] = version_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("task_id")

        doc_id = d.pop("doc_id")

        doc_filename = d.pop("doc_filename")

        doc_path = d.pop("doc_path")

        id = d.pop("id")

        metadata = ExtractResultOutMetadata.from_dict(d.pop("metadata"))

        top_chunks = []
        _top_chunks = d.pop("top_chunks")
        for top_chunks_item_data in _top_chunks:
            top_chunks_item = ExtractTopChunkOut.from_dict(top_chunks_item_data)

            top_chunks.append(top_chunks_item)

        validated_by = d.pop("validated_by", UNSET)

        validated_on: Union[Unset, datetime.datetime] = UNSET
        _validated_on = d.pop("validated_on", UNSET)
        if not isinstance(_validated_on, Unset):
            validated_on = isoparse(_validated_on)

        status = d.pop("status", UNSET)

        found = d.pop("found", UNSET)

        chunk_id = d.pop("chunk_id", UNSET)

        text = d.pop("text", UNSET)

        outdated = d.pop("outdated", UNSET)

        version_metadata: Union[ExtractResultOutVersionMetadata, Unset] = UNSET
        _version_metadata = d.pop("version_metadata", UNSET)
        if not isinstance(_version_metadata, Unset):
            version_metadata = ExtractResultOutVersionMetadata.from_dict(_version_metadata)

        extract_result_out = cls(
            task_id=task_id,
            doc_id=doc_id,
            doc_filename=doc_filename,
            doc_path=doc_path,
            id=id,
            metadata=metadata,
            top_chunks=top_chunks,
            validated_by=validated_by,
            validated_on=validated_on,
            status=status,
            found=found,
            chunk_id=chunk_id,
            text=text,
            outdated=outdated,
            version_metadata=version_metadata,
        )

        extract_result_out.additional_properties = d
        return extract_result_out

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
