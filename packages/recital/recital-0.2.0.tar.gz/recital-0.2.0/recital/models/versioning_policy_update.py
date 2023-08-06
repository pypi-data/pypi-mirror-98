from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VersioningPolicyUpdate")


@attr.s(auto_attribs=True)
class VersioningPolicyUpdate:
    """ Versioning policy update schema. """

    enabled: Union[Unset, bool] = True
    max_num_versions: Union[Unset, int] = 5
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        max_num_versions = self.max_num_versions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if max_num_versions is not UNSET:
            field_dict["max_num_versions"] = max_num_versions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        max_num_versions = d.pop("max_num_versions", UNSET)

        versioning_policy_update = cls(
            enabled=enabled,
            max_num_versions=max_num_versions,
        )

        versioning_policy_update.additional_properties = d
        return versioning_policy_update

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
