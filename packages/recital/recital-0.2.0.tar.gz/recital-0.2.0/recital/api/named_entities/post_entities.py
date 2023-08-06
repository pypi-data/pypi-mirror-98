from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.entity_in import EntityIn
from ...models.entity_in_db import EntityInDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[EntityIn],
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/{version_id}/entities/".format(client.base_url, version_id=version_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = EntityInDB.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
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
) -> Response[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
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
    json_body: List[EntityIn],
) -> Response[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[EntityIn],
) -> Optional[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
    """ Add named entities to a file version. Only services can access this route. """

    return sync_detailed(
        client=client,
        version_id=version_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[EntityIn],
) -> Response[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[EntityIn],
) -> Optional[Union[List[EntityInDB], None, None, None, HTTPValidationError]]:
    """ Add named entities to a file version. Only services can access this route. """

    return (
        await asyncio_detailed(
            client=client,
            version_id=version_id,
            json_body=json_body,
        )
    ).parsed
