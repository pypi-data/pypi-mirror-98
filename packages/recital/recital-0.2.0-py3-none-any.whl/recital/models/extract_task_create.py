from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extract_model_create import ExtractModelCreate
from ..models.task import Task
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractTaskCreate")


@attr.s(auto_attribs=True)
class ExtractTaskCreate:
    """ Extract task schema to be sent on POST /extract/models endpoint. """

    task: Task
    model: Union[ExtractModelCreate, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task = self.task.to_dict()

        model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task": task,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task = Task.from_dict(d.pop("task"))

        model: Union[ExtractModelCreate, Unset] = UNSET
        _model = d.pop("model", UNSET)
        if not isinstance(_model, Unset):
            model = ExtractModelCreate.from_dict(_model)

        extract_task_create = cls(
            task=task,
            model=model,
        )

        extract_task_create.additional_properties = d
        return extract_task_create

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
