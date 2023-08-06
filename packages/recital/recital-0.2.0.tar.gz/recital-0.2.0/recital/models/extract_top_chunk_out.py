from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExtractTopChunkOut")


@attr.s(auto_attribs=True)
class ExtractTopChunkOut:
    """ Top Chunk to add in DB. """

    result_id: int
    rank: int
    chunk_id: str
    page: int
    text: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result_id = self.result_id
        rank = self.rank
        chunk_id = self.chunk_id
        page = self.page
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result_id": result_id,
                "rank": rank,
                "chunk_id": chunk_id,
                "page": page,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result_id = d.pop("result_id")

        rank = d.pop("rank")

        chunk_id = d.pop("chunk_id")

        page = d.pop("page")

        text = d.pop("text")

        extract_top_chunk_out = cls(
            result_id=result_id,
            rank=rank,
            chunk_id=chunk_id,
            page=page,
            text=text,
        )

        extract_top_chunk_out.additional_properties = d
        return extract_top_chunk_out

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
