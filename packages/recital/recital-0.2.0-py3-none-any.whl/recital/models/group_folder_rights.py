from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.folder_right import FolderRight

T = TypeVar("T", bound="GroupFolderRights")


@attr.s(auto_attribs=True)
class GroupFolderRights:
    """ Group's folders rights. """

    rights: List[FolderRight]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rights = []
        for rights_item_data in self.rights:
            rights_item = rights_item_data.to_dict()

            rights.append(rights_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rights": rights,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rights = []
        _rights = d.pop("rights")
        for rights_item_data in _rights:
            rights_item = FolderRight.from_dict(rights_item_data)

            rights.append(rights_item)

        group_folder_rights = cls(
            rights=rights,
        )

        group_folder_rights.additional_properties = d
        return group_folder_rights

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
