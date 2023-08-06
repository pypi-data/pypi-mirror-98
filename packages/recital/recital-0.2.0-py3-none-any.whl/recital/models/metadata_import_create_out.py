import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_out import BackgroundTaskOut
from ..models.task_status import TaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataImportCreateOut")


@attr.s(auto_attribs=True)
class MetadataImportCreateOut:
    """ Schema representing the output from metadata import POST. """

    id: int
    org_id: int
    status: TaskStatus
    check_task_id: int
    temp_file_uuid: str
    report_id: int
    check_task: BackgroundTaskOut
    started_on: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        org_id = self.org_id
        status = self.status.value

        check_task_id = self.check_task_id
        temp_file_uuid = self.temp_file_uuid
        report_id = self.report_id
        check_task = self.check_task.to_dict()

        started_on: Union[Unset, str] = UNSET
        if not isinstance(self.started_on, Unset):
            started_on = self.started_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "status": status,
                "check_task_id": check_task_id,
                "temp_file_uuid": temp_file_uuid,
                "report_id": report_id,
                "check_task": check_task,
            }
        )
        if started_on is not UNSET:
            field_dict["started_on"] = started_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        org_id = d.pop("org_id")

        status = TaskStatus(d.pop("status"))

        check_task_id = d.pop("check_task_id")

        temp_file_uuid = d.pop("temp_file_uuid")

        report_id = d.pop("report_id")

        check_task = BackgroundTaskOut.from_dict(d.pop("check_task"))

        started_on: Union[Unset, datetime.datetime] = UNSET
        _started_on = d.pop("started_on", UNSET)
        if not isinstance(_started_on, Unset):
            started_on = isoparse(_started_on)

        metadata_import_create_out = cls(
            id=id,
            org_id=org_id,
            status=status,
            check_task_id=check_task_id,
            temp_file_uuid=temp_file_uuid,
            report_id=report_id,
            check_task=check_task,
            started_on=started_on,
        )

        metadata_import_create_out.additional_properties = d
        return metadata_import_create_out

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
