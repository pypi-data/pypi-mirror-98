import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.search_query_out_filters import SearchQueryOutFilters
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchQueryOut")


@attr.s(auto_attribs=True)
class SearchQueryOut:
    """ Search query schema to output from GET method. """

    user_id: int
    org_id: int
    queried_on: datetime.datetime
    id: int
    folder_ids: Union[Unset, List[int]] = UNSET
    output_fields: Union[Unset, List[str]] = UNSET
    filters: Union[SearchQueryOutFilters, Unset] = UNSET
    keywords: Union[Unset, List[str]] = UNSET
    keyword_op: Union[Unset, None] = UNSET
    keywords_only_query: Union[Unset, bool] = UNSET
    query: Union[Unset, str] = UNSET
    last_version: Union[Unset, bool] = True
    version_ids: Union[Unset, List[int]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        org_id = self.org_id
        queried_on = self.queried_on.isoformat()

        id = self.id
        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        output_fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.output_fields, Unset):
            output_fields = self.output_fields

        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        keywords: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        keyword_op = None

        keywords_only_query = self.keywords_only_query
        query = self.query
        last_version = self.last_version
        version_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.version_ids, Unset):
            version_ids = self.version_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "org_id": org_id,
                "queried_on": queried_on,
                "id": id,
            }
        )
        if folder_ids is not UNSET:
            field_dict["folder_ids"] = folder_ids
        if output_fields is not UNSET:
            field_dict["output_fields"] = output_fields
        if filters is not UNSET:
            field_dict["filters"] = filters
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if keyword_op is not UNSET:
            field_dict["keyword_op"] = keyword_op
        if keywords_only_query is not UNSET:
            field_dict["keywords_only_query"] = keywords_only_query
        if query is not UNSET:
            field_dict["query"] = query
        if last_version is not UNSET:
            field_dict["last_version"] = last_version
        if version_ids is not UNSET:
            field_dict["version_ids"] = version_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("user_id")

        org_id = d.pop("org_id")

        queried_on = isoparse(d.pop("queried_on"))

        id = d.pop("id")

        folder_ids = cast(List[int], d.pop("folder_ids", UNSET))

        output_fields = cast(List[str], d.pop("output_fields", UNSET))

        filters: Union[SearchQueryOutFilters, Unset] = UNSET
        _filters = d.pop("filters", UNSET)
        if not isinstance(_filters, Unset):
            filters = SearchQueryOutFilters.from_dict(_filters)

        keywords = cast(List[str], d.pop("keywords", UNSET))

        keyword_op = None

        keywords_only_query = d.pop("keywords_only_query", UNSET)

        query = d.pop("query", UNSET)

        last_version = d.pop("last_version", UNSET)

        version_ids = cast(List[int], d.pop("version_ids", UNSET))

        search_query_out = cls(
            user_id=user_id,
            org_id=org_id,
            queried_on=queried_on,
            id=id,
            folder_ids=folder_ids,
            output_fields=output_fields,
            filters=filters,
            keywords=keywords,
            keyword_op=keyword_op,
            keywords_only_query=keywords_only_query,
            query=query,
            last_version=last_version,
            version_ids=version_ids,
        )

        search_query_out.additional_properties = d
        return search_query_out

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
