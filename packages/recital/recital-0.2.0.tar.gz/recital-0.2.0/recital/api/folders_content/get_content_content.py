from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.content_content_out import ContentContentOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    folder_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/folders/{folder_id}/content/".format(client.base_url, folder_id=folder_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ContentContentOut.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    folder_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        folder_id=folder_id,
        limit=limit,
        offset=offset,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    folder_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    """Get list of items in a folder:
    - If the user is basic, they can only access folders they has rights on.
    - If the user is orgadmin, they can access all of their own organization's folders."""

    return sync_detailed(
        client=client,
        folder_id=folder_id,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    folder_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        folder_id=folder_id,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    folder_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[ContentContentOut, None, None, None, HTTPValidationError]]:
    """Get list of items in a folder:
    - If the user is basic, they can only access folders they has rights on.
    - If the user is orgadmin, they can access all of their own organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            folder_id=folder_id,
            limit=limit,
            offset=offset,
        )
    ).parsed
