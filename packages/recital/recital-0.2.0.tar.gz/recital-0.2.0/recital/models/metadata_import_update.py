from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.task_status import TaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataImportUpdate")


@attr.s(auto_attribs=True)
class MetadataImportUpdate:
    """ Metadata import PUT schema. """

    status: TaskStatus
    n_found_docs: Union[Unset, int] = UNSET
    n_notfound_docs: Union[Unset, int] = UNSET
    n_created_metadata: Union[Unset, int] = UNSET
    n_replaced_metadata: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        n_found_docs = self.n_found_docs
        n_notfound_docs = self.n_notfound_docs
        n_created_metadata = self.n_created_metadata
        n_replaced_metadata = self.n_replaced_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if n_found_docs is not UNSET:
            field_dict["n_found_docs"] = n_found_docs
        if n_notfound_docs is not UNSET:
            field_dict["n_notfound_docs"] = n_notfound_docs
        if n_created_metadata is not UNSET:
            field_dict["n_created_metadata"] = n_created_metadata
        if n_replaced_metadata is not UNSET:
            field_dict["n_replaced_metadata"] = n_replaced_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = TaskStatus(d.pop("status"))

        n_found_docs = d.pop("n_found_docs", UNSET)

        n_notfound_docs = d.pop("n_notfound_docs", UNSET)

        n_created_metadata = d.pop("n_created_metadata", UNSET)

        n_replaced_metadata = d.pop("n_replaced_metadata", UNSET)

        metadata_import_update = cls(
            status=status,
            n_found_docs=n_found_docs,
            n_notfound_docs=n_notfound_docs,
            n_created_metadata=n_created_metadata,
            n_replaced_metadata=n_replaced_metadata,
        )

        metadata_import_update.additional_properties = d
        return metadata_import_update

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
