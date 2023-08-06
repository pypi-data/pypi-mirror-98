from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.doc_count import DocCount
from ...models.http_validation_error import HTTPValidationError
from ...models.source_type import SourceType
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    source: SourceType,
    filters: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/tasks/doc_count/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_source = source.value

    params: Dict[str, Any] = {
        "source": json_source,
        "filters": filters,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DocCount, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = DocCount.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[DocCount, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    source: SourceType,
    filters: str,
) -> Response[Union[DocCount, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        source=source,
        filters=filters,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    source: SourceType,
    filters: str,
) -> Optional[Union[DocCount, None, None, None, HTTPValidationError]]:
    """Get the number of documents from an extract data source.

    Only orgadmins are allowed to access extract tasks.

    The id of the organization is inferred from the session token.

    If the source is:
    - \"folders\": filters must be a string list of folder ids to get documents from.
    Example: /?filters=1,2,3,4
    - \"metadata\": filters must a be the name of a metadata.

    In the latter case, if the metadata is:
    - binary: the route returns the number of documents for which the value is true.
    - non-binary: the route returns the number of documents for which the value exists."""

    return sync_detailed(
        client=client,
        source=source,
        filters=filters,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    source: SourceType,
    filters: str,
) -> Response[Union[DocCount, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        source=source,
        filters=filters,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    source: SourceType,
    filters: str,
) -> Optional[Union[DocCount, None, None, None, HTTPValidationError]]:
    """Get the number of documents from an extract data source.

    Only orgadmins are allowed to access extract tasks.

    The id of the organization is inferred from the session token.

    If the source is:
    - \"folders\": filters must be a string list of folder ids to get documents from.
    Example: /?filters=1,2,3,4
    - \"metadata\": filters must a be the name of a metadata.

    In the latter case, if the metadata is:
    - binary: the route returns the number of documents for which the value is true.
    - non-binary: the route returns the number of documents for which the value exists."""

    return (
        await asyncio_detailed(
            client=client,
            source=source,
            filters=filters,
        )
    ).parsed
