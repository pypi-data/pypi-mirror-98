from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.organization_admin_out import OrganizationAdminOut
from ..models.organization_out import OrganizationOut
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationCreateOut")


@attr.s(auto_attribs=True)
class OrganizationCreateOut:
    """ Organization schema to output from POST methods. """

    org: Union[OrganizationOut, Unset] = UNSET
    admin: Union[OrganizationAdminOut, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.org, Unset):
            org = self.org.to_dict()

        admin: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.admin, Unset):
            admin = self.admin.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if org is not UNSET:
            field_dict["org"] = org
        if admin is not UNSET:
            field_dict["admin"] = admin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org: Union[OrganizationOut, Unset] = UNSET
        _org = d.pop("org", UNSET)
        if not isinstance(_org, Unset):
            org = OrganizationOut.from_dict(_org)

        admin: Union[OrganizationAdminOut, Unset] = UNSET
        _admin = d.pop("admin", UNSET)
        if not isinstance(_admin, Unset):
            admin = OrganizationAdminOut.from_dict(_admin)

        organization_create_out = cls(
            org=org,
            admin=admin,
        )

        organization_create_out.additional_properties = d
        return organization_create_out

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
