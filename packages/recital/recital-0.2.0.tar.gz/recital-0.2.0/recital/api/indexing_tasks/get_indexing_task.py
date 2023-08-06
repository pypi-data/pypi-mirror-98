from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.indexing_task_out_expanded import IndexingTaskOutExpanded
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: int,
    details: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/tasks/indexing/{task_id}/".format(client.base_url, task_id=task_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "details": details,
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
) -> Optional[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = IndexingTaskOutExpanded.from_dict(response.json())

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
) -> Response[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
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
    details: Union[Unset, bool] = False,
) -> Response[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        details=details,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    task_id: int,
    details: Union[Unset, bool] = False,
) -> Optional[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
    """Get an indexing report.

    Users can only access the indexing tasks they ran.
    If the details parameter is set to true, the route will return details about the
    task (i.e., average size and document types), otherwise the route only returns
    basic information."""

    return sync_detailed(
        client=client,
        task_id=task_id,
        details=details,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    details: Union[Unset, bool] = False,
) -> Response[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        details=details,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: int,
    details: Union[Unset, bool] = False,
) -> Optional[Union[IndexingTaskOutExpanded, None, None, None, HTTPValidationError]]:
    """Get an indexing report.

    Users can only access the indexing tasks they ran.
    If the details parameter is set to true, the route will return details about the
    task (i.e., average size and document types), otherwise the route only returns
    basic information."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            details=details,
        )
    ).parsed
