from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="MetadataDateRange")


@attr.s(auto_attribs=True)
class MetadataDateRange:
    """ Metadata date range value validation schema. """

    gte: str
    lte: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gte = self.gte
        lte = self.lte

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gte": gte,
                "lte": lte,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        gte = d.pop("gte")

        lte = d.pop("lte")

        metadata_date_range = cls(
            gte=gte,
            lte=lte,
        )

        metadata_date_range.additional_properties = d
        return metadata_date_range

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
