from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FullPasswordPolicy")


@attr.s(auto_attribs=True)
class FullPasswordPolicy:
    """ Policy schema containing constant constraints as well. """

    org_id: int
    min_length: Union[Unset, int] = 8
    expiration: Union[Unset, int] = 90
    max_similarity: Union[Unset, float] = 0.6
    max_login_attempts: Union[Unset, int] = 3
    digit: Union[Unset, bool] = True
    upper: Union[Unset, bool] = True
    lower: Union[Unset, bool] = True
    special: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org_id = self.org_id
        min_length = self.min_length
        expiration = self.expiration
        max_similarity = self.max_similarity
        max_login_attempts = self.max_login_attempts
        digit = self.digit
        upper = self.upper
        lower = self.lower
        special = self.special

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_id": org_id,
            }
        )
        if min_length is not UNSET:
            field_dict["min_length"] = min_length
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if max_similarity is not UNSET:
            field_dict["max_similarity"] = max_similarity
        if max_login_attempts is not UNSET:
            field_dict["max_login_attempts"] = max_login_attempts
        if digit is not UNSET:
            field_dict["digit"] = digit
        if upper is not UNSET:
            field_dict["upper"] = upper
        if lower is not UNSET:
            field_dict["lower"] = lower
        if special is not UNSET:
            field_dict["special"] = special

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org_id = d.pop("org_id")

        min_length = d.pop("min_length", UNSET)

        expiration = d.pop("expiration", UNSET)

        max_similarity = d.pop("max_similarity", UNSET)

        max_login_attempts = d.pop("max_login_attempts", UNSET)

        digit = d.pop("digit", UNSET)

        upper = d.pop("upper", UNSET)

        lower = d.pop("lower", UNSET)

        special = d.pop("special", UNSET)

        full_password_policy = cls(
            org_id=org_id,
            min_length=min_length,
            expiration=expiration,
            max_similarity=max_similarity,
            max_login_attempts=max_login_attempts,
            digit=digit,
            upper=upper,
            lower=lower,
            special=special,
        )

        full_password_policy.additional_properties = d
        return full_password_policy

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
