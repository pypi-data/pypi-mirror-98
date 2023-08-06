from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.rights_create import RightsCreate

T = TypeVar("T", bound="RightsListOut")


@attr.s(auto_attribs=True)
class RightsListOut:
    """ Rights schema to output from GET methods. """

    groups: List[RightsCreate]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()

            groups.append(groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groups": groups,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = RightsCreate.from_dict(groups_item_data)

            groups.append(groups_item)

        rights_list_out = cls(
            groups=groups,
        )

        rights_list_out.additional_properties = d
        return rights_list_out

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
