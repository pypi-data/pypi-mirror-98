from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_result_validate_in import ExtractResultValidateIn
from ...models.extract_result_validate_out import ExtractResultValidateOut
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    result_id: int,
    json_body: ExtractResultValidateIn,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/results/{result_id}/validate/".format(client.base_url, result_id=result_id)

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
) -> Optional[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ExtractResultValidateOut.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 204:
        response_204 = None

        return response_204
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
) -> Response[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    result_id: int,
    json_body: ExtractResultValidateIn,
) -> Response[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        result_id=result_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    result_id: int,
    json_body: ExtractResultValidateIn,
) -> Optional[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    """Validates one or no prediction made for a document.

    Only orgadmins can validate predictions, and they can only validate the predictions of
    their own tasks.

    If none of the proposed chunks is the one we're looking for, we consider that no paragraph
    has been found in the document.

    When a manual validation occurs, only the validated chunk, if any, is kept,
    the other proposed chunks are deleted.

    If there are documents left to validate, the endpoint returns the next one.

    If there is no more document to validate, the endpoint returns a 204."""

    return sync_detailed(
        client=client,
        result_id=result_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    result_id: int,
    json_body: ExtractResultValidateIn,
) -> Response[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        result_id=result_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    result_id: int,
    json_body: ExtractResultValidateIn,
) -> Optional[Union[ExtractResultValidateOut, None, None, None, None, HTTPValidationError]]:
    """Validates one or no prediction made for a document.

    Only orgadmins can validate predictions, and they can only validate the predictions of
    their own tasks.

    If none of the proposed chunks is the one we're looking for, we consider that no paragraph
    has been found in the document.

    When a manual validation occurs, only the validated chunk, if any, is kept,
    the other proposed chunks are deleted.

    If there are documents left to validate, the endpoint returns the next one.

    If there is no more document to validate, the endpoint returns a 204."""

    return (
        await asyncio_detailed(
            client=client,
            result_id=result_id,
            json_body=json_body,
        )
    ).parsed
