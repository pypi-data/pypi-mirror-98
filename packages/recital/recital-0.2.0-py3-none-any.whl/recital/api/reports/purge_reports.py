from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/reports/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[None, None, None]]:
    """Purge expired reports, both in SQL database and in MongoDB.

    Only services are allowed to access this route."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[None, None, None]]:
    """Purge expired reports, both in SQL database and in MongoDB.

    Only services are allowed to access this route."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
