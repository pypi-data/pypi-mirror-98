from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import File

T = TypeVar("T", bound="BodyPostFileVersionApiV1FilesVersionsItem_ItemId__Post")


@attr.s(auto_attribs=True)
class BodyPostFileVersionApiV1FilesVersionsItem_ItemId__Post:
    """  """

    file_in: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_in = self.file_in.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_in": file_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_in = File(payload=BytesIO(d.pop("file_in")))

        body_post_file_version_api_v1_files_versions_item_item_id__post = cls(
            file_in=file_in,
        )

        body_post_file_version_api_v1_files_versions_item_item_id__post.additional_properties = d
        return body_post_file_version_api_v1_files_versions_item_item_id__post

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
