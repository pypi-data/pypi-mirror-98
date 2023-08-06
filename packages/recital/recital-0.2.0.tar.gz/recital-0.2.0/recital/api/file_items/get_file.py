from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.file_item_out_with_versions import FileItemOutWithVersions
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    file_id: int,
    versions: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/{file_id}/".format(client.base_url, file_id=file_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "versions": versions,
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
) -> Optional[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FileItemOutWithVersions.from_dict(response.json())

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
) -> Response[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    file_id: int,
    versions: Union[Unset, bool] = False,
) -> Response[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
        versions=versions,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    file_id: int,
    versions: Union[Unset, bool] = False,
) -> Optional[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    """Returns a single file item.

    If versions is set to true in the query arguments,
    the route also returns all of the file item versions.
    If not present, or if set to false, no version is returned.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return sync_detailed(
        client=client,
        file_id=file_id,
        versions=versions,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    file_id: int,
    versions: Union[Unset, bool] = False,
) -> Response[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
        versions=versions,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    file_id: int,
    versions: Union[Unset, bool] = False,
) -> Optional[Union[FileItemOutWithVersions, None, None, None, HTTPValidationError]]:
    """Returns a single file item.

    If versions is set to true in the query arguments,
    the route also returns all of the file item versions.
    If not present, or if set to false, no version is returned.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            file_id=file_id,
            versions=versions,
        )
    ).parsed
