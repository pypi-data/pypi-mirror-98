from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PasswordPolicyUpdate")


@attr.s(auto_attribs=True)
class PasswordPolicyUpdate:
    """ Policy update schema. """

    min_length: Union[Unset, int] = 8
    expiration: Union[Unset, int] = 90
    max_similarity: Union[Unset, float] = 0.6
    max_login_attempts: Union[Unset, int] = 3
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        min_length = self.min_length
        expiration = self.expiration
        max_similarity = self.max_similarity
        max_login_attempts = self.max_login_attempts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if min_length is not UNSET:
            field_dict["min_length"] = min_length
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if max_similarity is not UNSET:
            field_dict["max_similarity"] = max_similarity
        if max_login_attempts is not UNSET:
            field_dict["max_login_attempts"] = max_login_attempts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        min_length = d.pop("min_length", UNSET)

        expiration = d.pop("expiration", UNSET)

        max_similarity = d.pop("max_similarity", UNSET)

        max_login_attempts = d.pop("max_login_attempts", UNSET)

        password_policy_update = cls(
            min_length=min_length,
            expiration=expiration,
            max_similarity=max_similarity,
            max_login_attempts=max_login_attempts,
        )

        password_policy_update.additional_properties = d
        return password_policy_update

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
