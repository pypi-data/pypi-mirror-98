from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.chunk_result import ChunkResult
from ..models.search_result_chunks_chunks_item import SearchResultChunksChunksItem
from ..models.search_result_pipeline_logs import SearchResultPipelineLogs
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultChunks")


@attr.s(auto_attribs=True)
class SearchResultChunks:
    """ Schema for search result chunks. """

    query_id: int
    chunks: Union[List[ChunkResult], List[SearchResultChunksChunksItem]]
    pipeline_logs: SearchResultPipelineLogs
    stripped_query: List[str]
    suggested_query: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_id = self.query_id
        if isinstance(self.chunks, list):
            chunks = []
            for chunks_item_data in self.chunks:
                chunks_item = chunks_item_data.to_dict()

                chunks.append(chunks_item)

        else:
            chunks = []
            for chunks_item_data in self.chunks:
                chunks_item = chunks_item_data.to_dict()

                chunks.append(chunks_item)

        pipeline_logs = self.pipeline_logs.to_dict()

        stripped_query = self.stripped_query

        suggested_query = self.suggested_query

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_id": query_id,
                "chunks": chunks,
                "pipeline_logs": pipeline_logs,
                "stripped_query": stripped_query,
            }
        )
        if suggested_query is not UNSET:
            field_dict["suggested_query"] = suggested_query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_id = d.pop("query_id")

        def _parse_chunks(data: Any) -> Union[List[ChunkResult], List[SearchResultChunksChunksItem]]:
            data = None if isinstance(data, Unset) else data
            chunks: Union[List[ChunkResult], List[SearchResultChunksChunksItem]]
            try:
                chunks = UNSET
                _chunks = data
                for chunks_item_data in _chunks:
                    chunks_item = ChunkResult.from_dict(chunks_item_data)

                    chunks.append(chunks_item)

                return chunks
            except:  # noqa: E722
                pass
            chunks = UNSET
            _chunks = data
            for chunks_item_data in _chunks:
                chunks_item = SearchResultChunksChunksItem.from_dict(chunks_item_data)

                chunks.append(chunks_item)

            return chunks

        chunks = _parse_chunks(d.pop("chunks"))

        pipeline_logs = SearchResultPipelineLogs.from_dict(d.pop("pipeline_logs"))

        stripped_query = cast(List[str], d.pop("stripped_query"))

        suggested_query = d.pop("suggested_query", UNSET)

        search_result_chunks = cls(
            query_id=query_id,
            chunks=chunks,
            pipeline_logs=pipeline_logs,
            stripped_query=stripped_query,
            suggested_query=suggested_query,
        )

        search_result_chunks.additional_properties = d
        return search_result_chunks

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
