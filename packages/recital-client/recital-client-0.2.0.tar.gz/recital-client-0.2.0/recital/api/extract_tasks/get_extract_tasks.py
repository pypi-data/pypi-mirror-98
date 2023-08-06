from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_task_out import ExtractTaskOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = "",
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/tasks/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "name": name,
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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExtractTaskOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = "",
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        name=name,
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
    name: Union[Unset, str] = "",
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    """List the organization's extract tasks.

    Only orgadmins are allowed to access extract tasks.
    The organization's id is guessed from the session token.

    Tasks can be filtered by name.

    This route returns:
    - All of the organization's complete tasks
    - Ongoing tasks that the connected user has run (a user cannot see other users ongoing tasks)"""

    return sync_detailed(
        client=client,
        name=name,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = "",
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        name=name,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    name: Union[Unset, str] = "",
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[ExtractTaskOut], None, None, HTTPValidationError]]:
    """List the organization's extract tasks.

    Only orgadmins are allowed to access extract tasks.
    The organization's id is guessed from the session token.

    Tasks can be filtered by name.

    This route returns:
    - All of the organization's complete tasks
    - Ongoing tasks that the connected user has run (a user cannot see other users ongoing tasks)"""

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            limit=limit,
            offset=offset,
        )
    ).parsed
