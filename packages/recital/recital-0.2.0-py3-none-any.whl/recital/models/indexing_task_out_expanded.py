import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.background_task_out import BackgroundTaskOut
from ..models.doc_type import DocType
from ..models.indexing_error_in_db import IndexingErrorInDB
from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexingTaskOutExpanded")


@attr.s(auto_attribs=True)
class IndexingTaskOutExpanded:
    """ Output indexing task schema from GET methods. """

    bkg_task_id: int
    org_id: int
    run_by: int
    report_id: int
    id: int
    started_on: datetime.datetime
    background_task: BackgroundTaskOut
    errors: List[IndexingErrorInDB]
    finished_on: Union[Unset, datetime.datetime] = UNSET
    average_size: Union[Unset, int] = UNSET
    doc_types: Union[Unset, List[DocType]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bkg_task_id = self.bkg_task_id
        org_id = self.org_id
        run_by = self.run_by
        report_id = self.report_id
        id = self.id
        started_on = self.started_on.isoformat()

        background_task = self.background_task.to_dict()

        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()

            errors.append(errors_item)

        finished_on: Union[Unset, str] = UNSET
        if not isinstance(self.finished_on, Unset):
            finished_on = self.finished_on.isoformat()

        average_size = self.average_size
        doc_types: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.doc_types, Unset):
            doc_types = []
            for doc_types_item_data in self.doc_types:
                doc_types_item = doc_types_item_data.to_dict()

                doc_types.append(doc_types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bkg_task_id": bkg_task_id,
                "org_id": org_id,
                "run_by": run_by,
                "report_id": report_id,
                "id": id,
                "started_on": started_on,
                "background_task": background_task,
                "errors": errors,
            }
        )
        if finished_on is not UNSET:
            field_dict["finished_on"] = finished_on
        if average_size is not UNSET:
            field_dict["average_size"] = average_size
        if doc_types is not UNSET:
            field_dict["doc_types"] = doc_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bkg_task_id = d.pop("bkg_task_id")

        org_id = d.pop("org_id")

        run_by = d.pop("run_by")

        report_id = d.pop("report_id")

        id = d.pop("id")

        started_on = isoparse(d.pop("started_on"))

        background_task = BackgroundTaskOut.from_dict(d.pop("background_task"))

        errors = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = IndexingErrorInDB.from_dict(errors_item_data)

            errors.append(errors_item)

        finished_on: Union[Unset, datetime.datetime] = UNSET
        _finished_on = d.pop("finished_on", UNSET)
        if not isinstance(_finished_on, Unset):
            finished_on = isoparse(_finished_on)

        average_size = d.pop("average_size", UNSET)

        doc_types = []
        _doc_types = d.pop("doc_types", UNSET)
        for doc_types_item_data in _doc_types or []:
            doc_types_item = DocType.from_dict(doc_types_item_data)

            doc_types.append(doc_types_item)

        indexing_task_out_expanded = cls(
            bkg_task_id=bkg_task_id,
            org_id=org_id,
            run_by=run_by,
            report_id=report_id,
            id=id,
            started_on=started_on,
            background_task=background_task,
            errors=errors,
            finished_on=finished_on,
            average_size=average_size,
            doc_types=doc_types,
        )

        indexing_task_out_expanded.additional_properties = d
        return indexing_task_out_expanded

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
