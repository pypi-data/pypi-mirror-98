from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/search/history/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query_id": query_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query_id: Union[Unset, int] = UNSET,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query_id=query_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query_id: Union[Unset, int] = UNSET,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Delete the user's search history.

    If query_id is passed, only the specified query is deleted."""

    return sync_detailed(
        client=client,
        query_id=query_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query_id: Union[Unset, int] = UNSET,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query_id=query_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query_id: Union[Unset, int] = UNSET,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Delete the user's search history.

    If query_id is passed, only the specified query is deleted."""

    return (
        await asyncio_detailed(
            client=client,
            query_id=query_id,
        )
    ).parsed
