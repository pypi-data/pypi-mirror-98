import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.license_type import LicenseType
from ..models.product import Product

T = TypeVar("T", bound="OrganizationCreate")


@attr.s(auto_attribs=True)
class OrganizationCreate:
    """ Organization schema to receive from POST method. """

    name: str
    product: Product
    license_expires_on: datetime.datetime
    license_type: LicenseType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        product = self.product.value

        license_expires_on = self.license_expires_on.isoformat()

        license_type = self.license_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "product": product,
                "license_expires_on": license_expires_on,
                "license_type": license_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        product = Product(d.pop("product"))

        license_expires_on = isoparse(d.pop("license_expires_on"))

        license_type = LicenseType(d.pop("license_type"))

        organization_create = cls(
            name=name,
            product=product,
            license_expires_on=license_expires_on,
            license_type=license_type,
        )

        organization_create.additional_properties = d
        return organization_create

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
