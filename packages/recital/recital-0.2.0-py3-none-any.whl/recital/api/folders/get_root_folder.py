from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.id import ID
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/folders/root/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "org_id": org_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ID, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ID.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ID, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[ID, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[ID, None, None, HTTPValidationError]]:
    """Gets the root folder id.

    The endpoint does not expose information about the folder itself, just its id."""

    return sync_detailed(
        client=client,
        org_id=org_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[ID, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[ID, None, None, HTTPValidationError]]:
    """Gets the root folder id.

    The endpoint does not expose information about the folder itself, just its id."""

    return (
        await asyncio_detailed(
            client=client,
            org_id=org_id,
        )
    ).parsed
