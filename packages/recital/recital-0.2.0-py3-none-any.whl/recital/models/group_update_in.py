from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupUpdateIn")


@attr.s(auto_attribs=True)
class GroupUpdateIn:
    """ Group schema to receive from PUT method. """

    name: Union[Unset, str] = UNSET
    user_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        user_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.user_ids, Unset):
            user_ids = self.user_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if user_ids is not UNSET:
            field_dict["user_ids"] = user_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        user_ids = cast(List[int], d.pop("user_ids", UNSET))

        group_update_in = cls(
            name=name,
            user_ids=user_ids,
        )

        group_update_in.additional_properties = d
        return group_update_in

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
