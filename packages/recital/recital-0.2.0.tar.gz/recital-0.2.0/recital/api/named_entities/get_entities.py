from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.entity_in_db import EntityInDB
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_num: Union[Unset, int] = UNSET,
    chunk_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/{version_id}/entities/".format(client.base_url, version_id=version_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "page_num": page_num,
        "chunk_id": chunk_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[EntityInDB], None, None, None, None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EntityInDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = None

        return response_422
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[EntityInDB], None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_num: Union[Unset, int] = UNSET,
    chunk_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[EntityInDB], None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        page_num=page_num,
        chunk_id=chunk_id,
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
    version_id: int,
    page_num: Union[Unset, int] = UNSET,
    chunk_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[EntityInDB], None, None, None, None]]:
    """Get the named entities found in a file version.<br>
    If page_num is specified in the request, the route only returns the entities in the page.
    If chunk_id is specified in the request, the route only returns the entities in the chunk.
    The entities are detected during indexing.
    Consequently, it may be unavailable until indexing is done.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return sync_detailed(
        client=client,
        version_id=version_id,
        page_num=page_num,
        chunk_id=chunk_id,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_num: Union[Unset, int] = UNSET,
    chunk_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[EntityInDB], None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        page_num=page_num,
        chunk_id=chunk_id,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_num: Union[Unset, int] = UNSET,
    chunk_id: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[EntityInDB], None, None, None, None]]:
    """Get the named entities found in a file version.<br>
    If page_num is specified in the request, the route only returns the entities in the page.
    If chunk_id is specified in the request, the route only returns the entities in the chunk.
    The entities are detected during indexing.
    Consequently, it may be unavailable until indexing is done.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            version_id=version_id,
            page_num=page_num,
            chunk_id=chunk_id,
            limit=limit,
            offset=offset,
        )
    ).parsed
