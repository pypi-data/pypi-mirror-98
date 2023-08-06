from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import File

T = TypeVar("T", bound="BodyPostMetadataImportApiV1MetadataImport_Post")


@attr.s(auto_attribs=True)
class BodyPostMetadataImportApiV1MetadataImport_Post:
    """  """

    metadata_file: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata_file = self.metadata_file.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata_file": metadata_file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata_file = File(payload=BytesIO(d.pop("metadata_file")))

        body_post_metadata_import_api_v1_metadata_import_post = cls(
            metadata_file=metadata_file,
        )

        body_post_metadata_import_api_v1_metadata_import_post.additional_properties = d
        return body_post_metadata_import_api_v1_metadata_import_post

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
