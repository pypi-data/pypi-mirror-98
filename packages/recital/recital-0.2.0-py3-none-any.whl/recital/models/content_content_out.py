from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.file_item_out import FileItemOut
from ..models.folder_out import FolderOut

T = TypeVar("T", bound="ContentContentOut")


@attr.s(auto_attribs=True)
class ContentContentOut:
    """ Content schema to output from GET method. """

    folders: List[FolderOut]
    files: List[FileItemOut]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()

            files.append(files_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folders": folders,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = FolderOut.from_dict(folders_item_data)

            folders.append(folders_item)

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = FileItemOut.from_dict(files_item_data)

            files.append(files_item)

        content_content_out = cls(
            folders=folders,
            files=files,
        )

        content_content_out.additional_properties = d
        return content_content_out

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
