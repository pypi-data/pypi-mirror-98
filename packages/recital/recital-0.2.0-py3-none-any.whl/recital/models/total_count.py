from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="TotalCount")


@attr.s(auto_attribs=True)
class TotalCount:
    """ Total Count schema for the Get route. """

    type: str
    count: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        count = d.pop("count")

        total_count = cls(
            type=type,
            count=count,
        )

        total_count.additional_properties = d
        return total_count

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
