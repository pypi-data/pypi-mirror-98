from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.metadata_date_range import MetadataDateRange
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/{metadata_id}/value/".format(client.base_url, metadata_id=metadata_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "folder_id": folder_id,
        "version_id": version_id,
        "value": value,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 422:
        response_422 = None

        return response_422
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_id=metadata_id,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        value=value,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Assign a value to a metadata in some documents.
    Only orgadmins can assign values to metadata.
    - If the version parameter is passed,
        the specified value is assigned to the version.
    - If the folder parameter is passed,
        the specified value is assigned to all documents in the folder and its children.
    - If neither version or folder is passed,
        the value is assigned to all documents' current versions."""

    return sync_detailed(
        client=client,
        metadata_id=metadata_id,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        value=value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_id=metadata_id,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        value=value,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Optional[Union[None, None, None, None, None]]:
    """Assign a value to a metadata in some documents.
    Only orgadmins can assign values to metadata.
    - If the version parameter is passed,
        the specified value is assigned to the version.
    - If the folder parameter is passed,
        the specified value is assigned to all documents in the folder and its children.
    - If neither version or folder is passed,
        the value is assigned to all documents' current versions."""

    return (
        await asyncio_detailed(
            client=client,
            metadata_id=metadata_id,
            json_body=json_body,
            folder_id=folder_id,
            version_id=version_id,
            value=value,
        )
    ).parsed
