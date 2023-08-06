from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DisplayPolicy")


@attr.s(auto_attribs=True)
class DisplayPolicy:
    """ Display policy schema for endpoint returns. """

    see_explorer: bool
    org_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        see_explorer = self.see_explorer
        org_id = self.org_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "see_explorer": see_explorer,
                "org_id": org_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        see_explorer = d.pop("see_explorer")

        org_id = d.pop("org_id")

        display_policy = cls(
            see_explorer=see_explorer,
            org_id=org_id,
        )

        display_policy.additional_properties = d
        return display_policy

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
