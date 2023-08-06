from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.content_details_out import ContentDetailsOut
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    folder_id: int,
) -> Dict[str, Any]:
    url = "{}/api/v1/folders/{folder_id}/details/".format(client.base_url, folder_id=folder_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ContentDetailsOut.from_dict(response.json())

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
) -> Response[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    folder_id: int,
) -> Response[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        folder_id=folder_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    folder_id: int,
) -> Optional[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    """Get the details of a folder:
    - If the user is basic, they can only access folders they have rights on.
    - If the user is orgadmin, they can access all of their organization's folders."""

    return sync_detailed(
        client=client,
        folder_id=folder_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    folder_id: int,
) -> Response[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        folder_id=folder_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    folder_id: int,
) -> Optional[Union[ContentDetailsOut, None, None, None, HTTPValidationError]]:
    """Get the details of a folder:
    - If the user is basic, they can only access folders they have rights on.
    - If the user is orgadmin, they can access all of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            folder_id=folder_id,
        )
    ).parsed
