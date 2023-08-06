from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="EmailTemplateOut")


@attr.s(auto_attribs=True)
class EmailTemplateOut:
    """ Email Template schema for endpoints return. """

    display_name: str
    id: int
    internal_name: str
    subject: str
    body: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        display_name = self.display_name
        id = self.id
        internal_name = self.internal_name
        subject = self.subject
        body = self.body

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "id": id,
                "internal_name": internal_name,
                "subject": subject,
                "body": body,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        display_name = d.pop("display_name")

        id = d.pop("id")

        internal_name = d.pop("internal_name")

        subject = d.pop("subject")

        body = d.pop("body")

        email_template_out = cls(
            display_name=display_name,
            id=id,
            internal_name=internal_name,
            subject=subject,
            body=body,
        )

        email_template_out.additional_properties = d
        return email_template_out

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
