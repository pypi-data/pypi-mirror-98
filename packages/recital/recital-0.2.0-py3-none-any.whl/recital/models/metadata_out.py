from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metadata_source import MetadataSource
from ..models.metadata_type import MetadataType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataOut")


@attr.s(auto_attribs=True)
class MetadataOut:
    """ Metadata schema to output from GET methods. """

    name: str
    org_id: int
    value_type: MetadataType
    n_queries: int
    primary_filter: bool
    secondary_filter: bool
    chunks_results: bool
    sorting_metadata: bool
    id: int
    source: MetadataSource
    sample: Union[Unset, None] = UNSET
    nb_distinct_values: Union[Unset, int] = 0
    max_values: Union[Unset, int] = 20
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        org_id = self.org_id
        value_type = self.value_type.value

        n_queries = self.n_queries
        primary_filter = self.primary_filter
        secondary_filter = self.secondary_filter
        chunks_results = self.chunks_results
        sorting_metadata = self.sorting_metadata
        id = self.id
        source = self.source.value

        sample = None

        nb_distinct_values = self.nb_distinct_values
        max_values = self.max_values

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "org_id": org_id,
                "value_type": value_type,
                "n_queries": n_queries,
                "primary_filter": primary_filter,
                "secondary_filter": secondary_filter,
                "chunks_results": chunks_results,
                "sorting_metadata": sorting_metadata,
                "id": id,
                "source": source,
            }
        )
        if sample is not UNSET:
            field_dict["sample"] = sample
        if nb_distinct_values is not UNSET:
            field_dict["nb_distinct_values"] = nb_distinct_values
        if max_values is not UNSET:
            field_dict["max_values"] = max_values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        org_id = d.pop("org_id")

        value_type = MetadataType(d.pop("value_type"))

        n_queries = d.pop("n_queries")

        primary_filter = d.pop("primary_filter")

        secondary_filter = d.pop("secondary_filter")

        chunks_results = d.pop("chunks_results")

        sorting_metadata = d.pop("sorting_metadata")

        id = d.pop("id")

        source = MetadataSource(d.pop("source"))

        sample = None

        nb_distinct_values = d.pop("nb_distinct_values", UNSET)

        max_values = d.pop("max_values", UNSET)

        metadata_out = cls(
            name=name,
            org_id=org_id,
            value_type=value_type,
            n_queries=n_queries,
            primary_filter=primary_filter,
            secondary_filter=secondary_filter,
            chunks_results=chunks_results,
            sorting_metadata=sorting_metadata,
            id=id,
            source=source,
            sample=sample,
            nb_distinct_values=nb_distinct_values,
            max_values=max_values,
        )

        metadata_out.additional_properties = d
        return metadata_out

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
