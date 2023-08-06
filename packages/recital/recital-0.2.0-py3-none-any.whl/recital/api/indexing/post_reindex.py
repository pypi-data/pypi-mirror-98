from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v1/folders/{folder_id}/reindex/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None]]:
    if response.status_code == 501:
        response_501 = None

        return response_501
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[None, None, None, None]]:
    """Requests the reindexing of a folder.

    If the children parameter is set to true, folder's child hierarchy is also reindexed. If
    set to false or not present, only the specified folder should be reindexed.
    - If the user is basic, they cannot request a folder reindexing.
    - If the user is orgadmin, they can reindex all of their own organization's folders."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[None, None, None, None]]:
    """Requests the reindexing of a folder.

    If the children parameter is set to true, folder's child hierarchy is also reindexed. If
    set to false or not present, only the specified folder should be reindexed.
    - If the user is basic, they cannot request a folder reindexing.
    - If the user is orgadmin, they can reindex all of their own organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
