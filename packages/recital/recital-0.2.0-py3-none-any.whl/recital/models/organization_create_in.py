from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.organization_admin_in import OrganizationAdminIn
from ..models.organization_create import OrganizationCreate

T = TypeVar("T", bound="OrganizationCreateIn")


@attr.s(auto_attribs=True)
class OrganizationCreateIn:
    """ Organization schema for POST input. """

    org: OrganizationCreate
    admin: OrganizationAdminIn
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org = self.org.to_dict()

        admin = self.admin.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org": org,
                "admin": admin,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org = OrganizationCreate.from_dict(d.pop("org"))

        admin = OrganizationAdminIn.from_dict(d.pop("admin"))

        organization_create_in = cls(
            org=org,
            admin=admin,
        )

        organization_create_in.additional_properties = d
        return organization_create_in

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
