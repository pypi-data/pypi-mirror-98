from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_result_out import ExtractResultOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/results/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "task_id": task_id,
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
) -> Optional[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExtractResultOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
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
    task_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    """Get the results of an extract task.

    Only orgadmins can access tasks results.

    If the task is ongoing, they can only access their own tasks results."""

    return sync_detailed(
        client=client,
        task_id=task_id,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: int,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractResultOut], None, None, None, HTTPValidationError]]:
    """Get the results of an extract task.

    Only orgadmins can access tasks results.

    If the task is ongoing, they can only access their own tasks results."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            limit=limit,
            offset=offset,
        )
    ).parsed
