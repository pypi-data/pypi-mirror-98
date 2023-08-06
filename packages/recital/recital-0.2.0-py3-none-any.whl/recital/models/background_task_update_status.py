from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.background_task_update_status_info import BackgroundTaskUpdateStatusInfo
from ..models.task_status import TaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="BackgroundTaskUpdateStatus")


@attr.s(auto_attribs=True)
class BackgroundTaskUpdateStatus:
    """Background task schema for updating
    a task status and number of items to be processed.

    An optional report id can be specified."""

    status: TaskStatus
    total_items: Union[Unset, int] = UNSET
    info: Union[BackgroundTaskUpdateStatusInfo, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        total_items = self.total_items
        info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.info, Unset):
            info = self.info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if total_items is not UNSET:
            field_dict["total_items"] = total_items
        if info is not UNSET:
            field_dict["info"] = info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = TaskStatus(d.pop("status"))

        total_items = d.pop("total_items", UNSET)

        info: Union[BackgroundTaskUpdateStatusInfo, Unset] = UNSET
        _info = d.pop("info", UNSET)
        if not isinstance(_info, Unset):
            info = BackgroundTaskUpdateStatusInfo.from_dict(_info)

        background_task_update_status = cls(
            status=status,
            total_items=total_items,
            info=info,
        )

        background_task_update_status.additional_properties = d
        return background_task_update_status

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
