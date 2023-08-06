from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_model_create import ExtractModelCreate
from ...models.extract_model_out import ExtractModelOut
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ExtractModelCreate,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/models/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ExtractModelOut.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 409:
        response_409 = None

        return response_409
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractModelCreate,
) -> Response[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ExtractModelCreate,
) -> Optional[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    """Creates a new extract model.

    Only orgadmins are allowed to create extract models.
    The id of the organization is inferred from the session token.
    Two models cannot have the same name for the same organization."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractModelCreate,
) -> Response[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ExtractModelCreate,
) -> Optional[Union[ExtractModelOut, None, None, None, HTTPValidationError]]:
    """Creates a new extract model.

    Only orgadmins are allowed to create extract models.
    The id of the organization is inferred from the session token.
    Two models cannot have the same name for the same organization."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
