from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

import attr

from ..types import File

T = TypeVar("T", bound="BodyPutSynonymsApiV1SearchConfigSynonyms_Put")


@attr.s(auto_attribs=True)
class BodyPutSynonymsApiV1SearchConfigSynonyms_Put:
    """  """

    synonyms_in: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        synonyms_in = self.synonyms_in.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "synonyms_in": synonyms_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        synonyms_in = File(payload=BytesIO(d.pop("synonyms_in")))

        body_put_synonyms_api_v1_search_config_synonyms_put = cls(
            synonyms_in=synonyms_in,
        )

        body_put_synonyms_api_v1_search_config_synonyms_put.additional_properties = d
        return body_put_synonyms_api_v1_search_config_synonyms_put

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
