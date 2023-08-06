from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DocType")


@attr.s(auto_attribs=True)
class DocType:
    """ Output doc type schema for indexing task details. """

    n_docs: int
    type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        n_docs = self.n_docs
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "n_docs": n_docs,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        n_docs = d.pop("n_docs")

        type = d.pop("type")

        doc_type = cls(
            n_docs=n_docs,
            type=type,
        )

        doc_type.additional_properties = d
        return doc_type

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
