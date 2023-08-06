from typing import Dict

import attr
import requests

BASE_URL = "https://app-7ece9dd3-6c58-440f-abb5-0e37dce10740.cleverapps.io"


@attr.s(auto_attribs=True)
class Client:
    """ A class for keeping track of data related to the API """

    base_url: str = attr.ib(BASE_URL, kw_only=True)
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)

    def get_headers(self) -> Dict[str, str]:
        """ Get headers to be used in all endpoints """
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """ Get a new client matching this one with additional headers """
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """ Get a new client matching this one with additional cookies """
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """ Get a new client matching this one with a new timeout (in seconds) """
        return attr.evolve(self, timeout=timeout)


@attr.s(auto_attribs=True)
class AuthenticatedClient(Client):
    """ A Client which has been authenticated for use on secured endpoints """

    token: str

    def get_headers(self) -> Dict[str, str]:
        """ Get headers to be used in authenticated endpoints """
        return {"Authorization": f"Bearer {self.token}", **self.headers}


def RecitalClient(username: str, password: str) -> AuthenticatedClient:
    res = requests.post(
        f"{BASE_URL}/api/v1/login/",
        data={"username": username, "password": password},
    )
    if res.status_code != 200:
        raise ValueError("Credentials are not valid.")
    return AuthenticatedClient(token=res.json()["access_token"])
