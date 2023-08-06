import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.chunk_bookmark_in_coordinates import ChunkBookmarkInCoordinates
from ..models.chunk_bookmark_in_query import ChunkBookmarkInQuery
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChunkBookmarkIn")


@attr.s(auto_attribs=True)
class ChunkBookmarkIn:
    """ Chunk bookmark schema to receive from the GET method. """

    collection_id: int
    id: int
    query: ChunkBookmarkInQuery
    version_id: int
    chunk_id: str
    chunk_text: str
    created_on: datetime.datetime
    from_semantic: bool
    coordinates: Union[ChunkBookmarkInCoordinates, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_id = self.collection_id
        id = self.id
        query = self.query.to_dict()

        version_id = self.version_id
        chunk_id = self.chunk_id
        chunk_text = self.chunk_text
        created_on = self.created_on.isoformat()

        from_semantic = self.from_semantic
        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_id": collection_id,
                "id": id,
                "query": query,
                "version_id": version_id,
                "chunk_id": chunk_id,
                "chunk_text": chunk_text,
                "created_on": created_on,
                "from_semantic": from_semantic,
            }
        )
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_id = d.pop("collection_id")

        id = d.pop("id")

        query = ChunkBookmarkInQuery.from_dict(d.pop("query"))

        version_id = d.pop("version_id")

        chunk_id = d.pop("chunk_id")

        chunk_text = d.pop("chunk_text")

        created_on = isoparse(d.pop("created_on"))

        from_semantic = d.pop("from_semantic")

        coordinates: Union[ChunkBookmarkInCoordinates, Unset] = UNSET
        _coordinates = d.pop("coordinates", UNSET)
        if not isinstance(_coordinates, Unset):
            coordinates = ChunkBookmarkInCoordinates.from_dict(_coordinates)

        chunk_bookmark_in = cls(
            collection_id=collection_id,
            id=id,
            query=query,
            version_id=version_id,
            chunk_id=chunk_id,
            chunk_text=chunk_text,
            created_on=created_on,
            from_semantic=from_semantic,
            coordinates=coordinates,
        )

        chunk_bookmark_in.additional_properties = d
        return chunk_bookmark_in

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
