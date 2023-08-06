from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.value_type import ValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractValueConfig")


@attr.s(auto_attribs=True)
class ExtractValueConfig:
    """ Value extraction configuration schema for extract models. """

    value_type: ValueType
    value: str
    all_values: bool
    keywords: List[str]
    words_around: List[str]
    keywords_operator: Union[Unset, None] = UNSET
    keywords_scope: Union[Unset, None] = UNSET
    start_page: Union[Unset, int] = UNSET
    end_page: Union[Unset, int] = UNSET
    words_direction: Union[Unset, None] = UNSET
    words_range: Union[Unset, int] = 10
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value_type = self.value_type.value

        value = self.value
        all_values = self.all_values
        keywords = self.keywords

        words_around = self.words_around

        keywords_operator = None

        keywords_scope = None

        start_page = self.start_page
        end_page = self.end_page
        words_direction = None

        words_range = self.words_range

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value_type": value_type,
                "value": value,
                "all_values": all_values,
                "keywords": keywords,
                "words_around": words_around,
            }
        )
        if keywords_operator is not UNSET:
            field_dict["keywords_operator"] = keywords_operator
        if keywords_scope is not UNSET:
            field_dict["keywords_scope"] = keywords_scope
        if start_page is not UNSET:
            field_dict["start_page"] = start_page
        if end_page is not UNSET:
            field_dict["end_page"] = end_page
        if words_direction is not UNSET:
            field_dict["words_direction"] = words_direction
        if words_range is not UNSET:
            field_dict["words_range"] = words_range

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value_type = ValueType(d.pop("value_type"))

        value = d.pop("value")

        all_values = d.pop("all_values")

        keywords = cast(List[str], d.pop("keywords"))

        words_around = cast(List[str], d.pop("words_around"))

        keywords_operator = None

        keywords_scope = None

        start_page = d.pop("start_page", UNSET)

        end_page = d.pop("end_page", UNSET)

        words_direction = None

        words_range = d.pop("words_range", UNSET)

        extract_value_config = cls(
            value_type=value_type,
            value=value,
            all_values=all_values,
            keywords=keywords,
            words_around=words_around,
            keywords_operator=keywords_operator,
            keywords_scope=keywords_scope,
            start_page=start_page,
            end_page=end_page,
            words_direction=words_direction,
            words_range=words_range,
        )

        extract_value_config.additional_properties = d
        return extract_value_config

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
