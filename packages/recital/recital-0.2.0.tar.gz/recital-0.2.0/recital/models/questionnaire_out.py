import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.questionnaire_out_source_query import QuestionnaireOutSourceQuery
from ..models.questionnaire_status import QuestionnaireStatus
from ..models.source_filters import SourceFilters
from ..models.source_type import SourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="QuestionnaireOut")


@attr.s(auto_attribs=True)
class QuestionnaireOut:
    """ Questionnaire schema for API return. """

    model_id: int
    org_id: int
    name: str
    created_by_id: int
    created_by_name: str
    source_type: SourceType
    source_filters: SourceFilters
    source_query: QuestionnaireOutSourceQuery
    id: int
    status: QuestionnaireStatus
    created_on: datetime.datetime
    total_documents: Union[Unset, int] = 0
    per_folder: Union[Unset, bool] = False
    completed_on: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        model_id = self.model_id
        org_id = self.org_id
        name = self.name
        created_by_id = self.created_by_id
        created_by_name = self.created_by_name
        source_type = self.source_type.value

        source_filters = self.source_filters.to_dict()

        source_query = self.source_query.to_dict()

        id = self.id
        status = self.status.value

        created_on = self.created_on.isoformat()

        total_documents = self.total_documents
        per_folder = self.per_folder
        completed_on: Union[Unset, str] = UNSET
        if not isinstance(self.completed_on, Unset):
            completed_on = self.completed_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_id": model_id,
                "org_id": org_id,
                "name": name,
                "created_by_id": created_by_id,
                "created_by_name": created_by_name,
                "source_type": source_type,
                "source_filters": source_filters,
                "source_query": source_query,
                "id": id,
                "status": status,
                "created_on": created_on,
            }
        )
        if total_documents is not UNSET:
            field_dict["total_documents"] = total_documents
        if per_folder is not UNSET:
            field_dict["per_folder"] = per_folder
        if completed_on is not UNSET:
            field_dict["completed_on"] = completed_on

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = d.pop("model_id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        created_by_id = d.pop("created_by_id")

        created_by_name = d.pop("created_by_name")

        source_type = SourceType(d.pop("source_type"))

        source_filters = SourceFilters.from_dict(d.pop("source_filters"))

        source_query = QuestionnaireOutSourceQuery.from_dict(d.pop("source_query"))

        id = d.pop("id")

        status = QuestionnaireStatus(d.pop("status"))

        created_on = isoparse(d.pop("created_on"))

        total_documents = d.pop("total_documents", UNSET)

        per_folder = d.pop("per_folder", UNSET)

        completed_on: Union[Unset, datetime.datetime] = UNSET
        _completed_on = d.pop("completed_on", UNSET)
        if not isinstance(_completed_on, Unset):
            completed_on = isoparse(_completed_on)

        questionnaire_out = cls(
            model_id=model_id,
            org_id=org_id,
            name=name,
            created_by_id=created_by_id,
            created_by_name=created_by_name,
            source_type=source_type,
            source_filters=source_filters,
            source_query=source_query,
            id=id,
            status=status,
            created_on=created_on,
            total_documents=total_documents,
            per_folder=per_folder,
            completed_on=completed_on,
        )

        questionnaire_out.additional_properties = d
        return questionnaire_out

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
