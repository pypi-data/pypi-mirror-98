from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.doc_source import DocSource
from ..models.extract_type import ExtractType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Task")


@attr.s(auto_attribs=True)
class Task:
    """ Task schema. """

    type: ExtractType
    name: str
    doc_source: DocSource
    per_folder: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        name = self.name
        doc_source = self.doc_source.to_dict()

        per_folder = self.per_folder

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "name": name,
                "doc_source": doc_source,
            }
        )
        if per_folder is not UNSET:
            field_dict["per_folder"] = per_folder

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ExtractType(d.pop("type"))

        name = d.pop("name")

        doc_source = DocSource.from_dict(d.pop("doc_source"))

        per_folder = d.pop("per_folder", UNSET)

        task = cls(
            type=type,
            name=name,
            doc_source=doc_source,
            per_folder=per_folder,
        )

        task.additional_properties = d
        return task

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
