from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_model_out import ExtractModelOut
from ...models.extract_type import ExtractType
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    extract_type: Union[Unset, ExtractType] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/models/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_extract_type: Union[Unset, ExtractType] = UNSET
    if not isinstance(extract_type, Unset):
        json_extract_type = extract_type

    params: Dict[str, Any] = {
        "extract_type": json_extract_type,
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
) -> Optional[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExtractModelOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    extract_type: Union[Unset, ExtractType] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        extract_type=extract_type,
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
    extract_type: Union[Unset, ExtractType] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    """List available extract models.

    Only orgadmins are allowed to access extract models.
    The id of the organization is inferred from the session token."""

    return sync_detailed(
        client=client,
        extract_type=extract_type,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    extract_type: Union[Unset, ExtractType] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        extract_type=extract_type,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    extract_type: Union[Unset, ExtractType] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractModelOut], None, None, HTTPValidationError]]:
    """List available extract models.

    Only orgadmins are allowed to access extract models.
    The id of the organization is inferred from the session token."""

    return (
        await asyncio_detailed(
            client=client,
            extract_type=extract_type,
            limit=limit,
            offset=offset,
        )
    ).parsed
