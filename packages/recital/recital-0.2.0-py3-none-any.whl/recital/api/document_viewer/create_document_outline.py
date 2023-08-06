from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.create_document_outline_json_body_item import CreateDocumentOutlineJsonBodyItem
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[CreateDocumentOutlineJsonBodyItem],
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/{version_id}/outline/".format(client.base_url, version_id=version_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
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
    version_id: int,
    json_body: List[CreateDocumentOutlineJsonBodyItem],
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
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
    json_body: List[CreateDocumentOutlineJsonBodyItem],
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Create the document outline of a file version.
    - Only services can create document outlines."""

    return sync_detailed(
        client=client,
        version_id=version_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    json_body: List[CreateDocumentOutlineJsonBodyItem],
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
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
    json_body: List[CreateDocumentOutlineJsonBodyItem],
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Create the document outline of a file version.
    - Only services can create document outlines."""

    return (
        await asyncio_detailed(
            client=client,
            version_id=version_id,
            json_body=json_body,
        )
    ).parsed
