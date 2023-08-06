import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.group_out import GroupOut
from ..models.timezone import Timezone
from ..models.user_language import UserLanguage
from ..models.user_role import UserRole
from ..models.user_status import UserStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserOut")


@attr.s(auto_attribs=True)
class UserOut:
    """ User schema to output from GET methods. """

    id: int
    org_id: int
    first_name: str
    last_name: str
    email: str
    language: UserLanguage
    timezone: Timezone
    password_updated_on: datetime.datetime
    role: UserRole
    org_contact: bool
    status: UserStatus
    active: bool
    created_on: datetime.datetime
    last_login_on: Union[Unset, datetime.datetime] = UNSET
    groups: Union[Unset, List[GroupOut]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        org_id = self.org_id
        first_name = self.first_name
        last_name = self.last_name
        email = self.email
        language = self.language.value

        timezone = self.timezone.value

        password_updated_on = self.password_updated_on.isoformat()

        role = self.role.value

        org_contact = self.org_contact
        status = self.status.value

        active = self.active
        created_on = self.created_on.isoformat()

        last_login_on: Union[Unset, str] = UNSET
        if not isinstance(self.last_login_on, Unset):
            last_login_on = self.last_login_on.isoformat()

        groups: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "language": language,
                "timezone": timezone,
                "password_updated_on": password_updated_on,
                "role": role,
                "org_contact": org_contact,
                "status": status,
                "active": active,
                "created_on": created_on,
            }
        )
        if last_login_on is not UNSET:
            field_dict["last_login_on"] = last_login_on
        if groups is not UNSET:
            field_dict["groups"] = groups

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        org_id = d.pop("org_id")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        email = d.pop("email")

        language = UserLanguage(d.pop("language"))

        timezone = Timezone(d.pop("timezone"))

        password_updated_on = isoparse(d.pop("password_updated_on"))

        role = UserRole(d.pop("role"))

        org_contact = d.pop("org_contact")

        status = UserStatus(d.pop("status"))

        active = d.pop("active")

        created_on = isoparse(d.pop("created_on"))

        last_login_on: Union[Unset, datetime.datetime] = UNSET
        _last_login_on = d.pop("last_login_on", UNSET)
        if not isinstance(_last_login_on, Unset):
            last_login_on = isoparse(_last_login_on)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = GroupOut.from_dict(groups_item_data)

            groups.append(groups_item)

        user_out = cls(
            id=id,
            org_id=org_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            language=language,
            timezone=timezone,
            password_updated_on=password_updated_on,
            role=role,
            org_contact=org_contact,
            status=status,
            active=active,
            created_on=created_on,
            last_login_on=last_login_on,
            groups=groups,
        )

        user_out.additional_properties = d
        return user_out

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
