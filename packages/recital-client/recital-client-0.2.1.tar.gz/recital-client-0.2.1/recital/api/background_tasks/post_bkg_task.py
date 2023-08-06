from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.background_task_in import BackgroundTaskIn
from ...models.background_task_out import BackgroundTaskOut
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: BackgroundTaskIn,
) -> Dict[str, Any]:
    url = "{}/api/v1/tasks/".format(client.base_url)

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
) -> Optional[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = BackgroundTaskOut.from_dict(response.json())

        return response_201
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


def _build_response(
    *, response: httpx.Response
) -> Response[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BackgroundTaskIn,
) -> Response[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
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
    json_body: BackgroundTaskIn,
) -> Optional[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
    """Creates a background task.

    Only services are allowed to use this route."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BackgroundTaskIn,
) -> Response[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
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
    json_body: BackgroundTaskIn,
) -> Optional[Union[BackgroundTaskOut, None, None, None, HTTPValidationError]]:
    """Creates a background task.

    Only services are allowed to use this route."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
