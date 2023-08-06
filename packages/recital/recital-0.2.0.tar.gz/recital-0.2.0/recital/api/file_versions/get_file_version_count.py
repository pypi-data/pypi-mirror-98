from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.doc_count import DocCount
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/count/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DocCount, None, None]]:
    if response.status_code == 200:
        response_200 = DocCount.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DocCount, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[DocCount, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DocCount, None, None]]:
    """Get a total count of document versions.

    - For orgadmins, the route returns the total number of document versions in the organization.
    - For basic users, the route returns the number of document versions they have rights on."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[DocCount, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DocCount, None, None]]:
    """Get a total count of document versions.

    - For orgadmins, the route returns the total number of document versions in the organization.
    - For basic users, the route returns the number of document versions they have rights on."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
