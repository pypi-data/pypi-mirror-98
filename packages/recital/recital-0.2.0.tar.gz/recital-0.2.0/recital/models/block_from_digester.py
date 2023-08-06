from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BlockFromDigester")


@attr.s(auto_attribs=True)
class BlockFromDigester:
    """ Chunk block description """

    page_number: int
    bbox: Union[Unset, List[None]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_number = self.page_number
        bbox: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.bbox, Unset):
            bbox = []
            for bbox_item_data in self.bbox:
                bbox_item = None

                bbox.append(bbox_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page_number": page_number,
            }
        )
        if bbox is not UNSET:
            field_dict["bbox"] = bbox

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page_number = d.pop("page_number")

        bbox = []
        _bbox = d.pop("bbox", UNSET)
        for bbox_item_data in _bbox or []:
            bbox_item = None

            bbox.append(bbox_item)

        block_from_digester = cls(
            page_number=page_number,
            bbox=bbox,
        )

        block_from_digester.additional_properties = d
        return block_from_digester

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
