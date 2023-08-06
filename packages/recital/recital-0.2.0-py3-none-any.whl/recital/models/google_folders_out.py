from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.google_drive_entity import GoogleDriveEntity
from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleFoldersOut")


@attr.s(auto_attribs=True)
class GoogleFoldersOut:
    """ Google Drive folders model returned from the API. """

    folders: List[GoogleDriveEntity]
    next_page_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folders": folders,
            }
        )
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = GoogleDriveEntity.from_dict(folders_item_data)

            folders.append(folders_item)

        next_page_token = d.pop("next_page_token", UNSET)

        google_folders_out = cls(
            folders=folders,
            next_page_token=next_page_token,
        )

        google_folders_out.additional_properties = d
        return google_folders_out

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
