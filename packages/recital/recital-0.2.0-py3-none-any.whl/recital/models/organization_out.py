import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.product import Product
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationOut")


@attr.s(auto_attribs=True)
class OrganizationOut:
    """ Organization schema to output from GET methods. """

    id: int
    n_users: int
    n_groups: int
    name: Union[Unset, str] = UNSET
    product: Union[Unset, Product] = UNSET
    license_expires_on: Union[Unset, datetime.datetime] = UNSET
    license_type: Union[Unset, str] = UNSET
    n_docs: Union[Unset, int] = 0
    two_factor: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        n_users = self.n_users
        n_groups = self.n_groups
        name = self.name
        product: Union[Unset, Product] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product

        license_expires_on: Union[Unset, str] = UNSET
        if not isinstance(self.license_expires_on, Unset):
            license_expires_on = self.license_expires_on.isoformat()

        license_type = self.license_type
        n_docs = self.n_docs
        two_factor = self.two_factor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "n_users": n_users,
                "n_groups": n_groups,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if product is not UNSET:
            field_dict["product"] = product
        if license_expires_on is not UNSET:
            field_dict["license_expires_on"] = license_expires_on
        if license_type is not UNSET:
            field_dict["license_type"] = license_type
        if n_docs is not UNSET:
            field_dict["n_docs"] = n_docs
        if two_factor is not UNSET:
            field_dict["two_factor"] = two_factor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        n_users = d.pop("n_users")

        n_groups = d.pop("n_groups")

        name = d.pop("name", UNSET)

        product: Union[Unset, Product] = UNSET
        _product = d.pop("product", UNSET)
        if not isinstance(_product, Unset):
            product = Product(_product)

        license_expires_on: Union[Unset, datetime.datetime] = UNSET
        _license_expires_on = d.pop("license_expires_on", UNSET)
        if not isinstance(_license_expires_on, Unset):
            license_expires_on = isoparse(_license_expires_on)

        license_type = d.pop("license_type", UNSET)

        n_docs = d.pop("n_docs", UNSET)

        two_factor = d.pop("two_factor", UNSET)

        organization_out = cls(
            id=id,
            n_users=n_users,
            n_groups=n_groups,
            name=name,
            product=product,
            license_expires_on=license_expires_on,
            license_type=license_type,
            n_docs=n_docs,
            two_factor=two_factor,
        )

        organization_out.additional_properties = d
        return organization_out

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
