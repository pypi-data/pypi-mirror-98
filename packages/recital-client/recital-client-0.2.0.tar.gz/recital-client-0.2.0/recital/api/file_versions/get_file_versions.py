from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.version import Version
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    item_id: int,
    only_indexed: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/item/{item_id}/".format(client.base_url, item_id=item_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "only_indexed": only_indexed,
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
) -> Optional[Union[List[Version], None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Version.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[List[Version], None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    item_id: int,
    only_indexed: Union[Unset, bool] = False,
) -> Response[Union[List[Version], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        item_id=item_id,
        only_indexed=only_indexed,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    item_id: int,
    only_indexed: Union[Unset, bool] = False,
) -> Optional[Union[List[Version], None, None, None, HTTPValidationError]]:
    """List the versions of a file item.
    - If the user is basic, they can only access files in folders they have rights on.
    - If the user is orgadmin, they can access files in all of their organization's folders.

    If the `only_indexed` optional parameter is set to `True`, the endpoint returns only
    indexed file versions."""

    return sync_detailed(
        client=client,
        item_id=item_id,
        only_indexed=only_indexed,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    item_id: int,
    only_indexed: Union[Unset, bool] = False,
) -> Response[Union[List[Version], None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        item_id=item_id,
        only_indexed=only_indexed,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    item_id: int,
    only_indexed: Union[Unset, bool] = False,
) -> Optional[Union[List[Version], None, None, None, HTTPValidationError]]:
    """List the versions of a file item.
    - If the user is basic, they can only access files in folders they have rights on.
    - If the user is orgadmin, they can access files in all of their organization's folders.

    If the `only_indexed` optional parameter is set to `True`, the endpoint returns only
    indexed file versions."""

    return (
        await asyncio_detailed(
            client=client,
            item_id=item_id,
            only_indexed=only_indexed,
        )
    ).parsed
