import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportOutput")


@attr.s(auto_attribs=True)
class ReportOutput:
    """ Report schema to output from GET methods. """

    name: str
    expires_on: datetime.datetime
    id: int
    user_id: int
    created_on: datetime.datetime
    bkgd_task_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        expires_on = self.expires_on.isoformat()

        id = self.id
        user_id = self.user_id
        created_on = self.created_on.isoformat()

        bkgd_task_id = self.bkgd_task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "expires_on": expires_on,
                "id": id,
                "user_id": user_id,
                "created_on": created_on,
            }
        )
        if bkgd_task_id is not UNSET:
            field_dict["bkgd_task_id"] = bkgd_task_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        expires_on = isoparse(d.pop("expires_on"))

        id = d.pop("id")

        user_id = d.pop("user_id")

        created_on = isoparse(d.pop("created_on"))

        bkgd_task_id = d.pop("bkgd_task_id", UNSET)

        report_output = cls(
            name=name,
            expires_on=expires_on,
            id=id,
            user_id=user_id,
            created_on=created_on,
            bkgd_task_id=bkgd_task_id,
        )

        report_output.additional_properties = d
        return report_output

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
