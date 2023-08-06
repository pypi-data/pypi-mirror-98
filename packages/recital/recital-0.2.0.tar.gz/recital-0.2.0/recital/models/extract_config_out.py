from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExtractConfigOut")


@attr.s(auto_attribs=True)
class ExtractConfigOut:
    """ Extract configuration schema to be returned from the API. """

    n_proposed_paragraphs: int
    n_auto_paragraphs: int
    org_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        n_proposed_paragraphs = self.n_proposed_paragraphs
        n_auto_paragraphs = self.n_auto_paragraphs
        org_id = self.org_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "n_proposed_paragraphs": n_proposed_paragraphs,
                "n_auto_paragraphs": n_auto_paragraphs,
                "org_id": org_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        n_proposed_paragraphs = d.pop("n_proposed_paragraphs")

        n_auto_paragraphs = d.pop("n_auto_paragraphs")

        org_id = d.pop("org_id")

        extract_config_out = cls(
            n_proposed_paragraphs=n_proposed_paragraphs,
            n_auto_paragraphs=n_auto_paragraphs,
            org_id=org_id,
        )

        extract_config_out.additional_properties = d
        return extract_config_out

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
