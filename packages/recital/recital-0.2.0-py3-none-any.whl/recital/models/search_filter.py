from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.filter_operator import FilterOperator
from ..models.metadata_date_range import MetadataDateRange
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchFilter")


@attr.s(auto_attribs=True)
class SearchFilter:
    """ Search metadata schema. """

    operator: FilterOperator
    value: Union[Unset, str, List[str], MetadataDateRange, List[MetadataDateRange]] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operator = self.operator.value

        value: Union[Unset, str, List[str], MetadataDateRange, List[MetadataDateRange]]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value

        elif isinstance(self.value, MetadataDateRange):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value.to_dict()

        elif isinstance(self.value, list):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = []
                for value_item_data in self.value:
                    value_item = value_item_data.to_dict()

                    value.append(value_item)

        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = FilterOperator(d.pop("operator"))

        def _parse_value(data: Any) -> Union[Unset, str, List[str], MetadataDateRange, List[MetadataDateRange]]:
            data = None if isinstance(data, Unset) else data
            value: Union[Unset, str, List[str], MetadataDateRange, List[MetadataDateRange]]
            try:
                value = cast(List[str], data)

                return value
            except:  # noqa: E722
                pass
            try:
                value = UNSET
                _value = data
                if not isinstance(_value, Unset):
                    value = MetadataDateRange.from_dict(_value)

                return value
            except:  # noqa: E722
                pass
            try:
                value = UNSET
                _value = data
                for value_item_data in _value or []:
                    value_item = MetadataDateRange.from_dict(value_item_data)

                    value.append(value_item)

                return value
            except:  # noqa: E722
                pass
            return cast(Union[Unset, str, List[str], MetadataDateRange, List[MetadataDateRange]], data)

        value = _parse_value(d.pop("value", UNSET))

        search_filter = cls(
            operator=operator,
            value=value,
        )

        search_filter.additional_properties = d
        return search_filter

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
