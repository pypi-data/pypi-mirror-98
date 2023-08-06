from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_config_out import ExtractConfigOut
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/configuration/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ExtractConfigOut, None, None]]:
    if response.status_code == 200:
        response_200 = ExtractConfigOut.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ExtractConfigOut, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ExtractConfigOut, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ExtractConfigOut, None, None]]:
    """Access the organization extract configuration.

    Only orgadmins can see the extract configuration.
    The id of the organization is inferred from the session token."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ExtractConfigOut, None, None]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ExtractConfigOut, None, None]]:
    """Access the organization extract configuration.

    Only orgadmins can see the extract configuration.
    The id of the organization is inferred from the session token."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
