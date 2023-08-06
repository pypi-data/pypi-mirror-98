from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.folder_out import FolderOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    exact: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/folders/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "org_id": org_id,
        "path": path,
        "name": name,
        "exact": exact,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[FolderOut], None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FolderOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[FolderOut], None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    exact: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[FolderOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
        path=path,
        name=name,
        exact=exact,
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
    org_id: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    exact: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[FolderOut], None, None, HTTPValidationError]]:
    """Gets a page of all folders the user has access to:
    - If the user is basic, they can only access folders they had rights on.
    - If the user is orgadmin, they can access all of their own organization's folders.

    Additionally, search query parameters can be provided. In case 'path' is provided,
    'name' is ignored. An extra parameter 'exact' can be set if the exact folder path or
    name is needed from the folders."""

    return sync_detailed(
        client=client,
        org_id=org_id,
        path=path,
        name=name,
        exact=exact,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    exact: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[List[FolderOut], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        org_id=org_id,
        path=path,
        name=name,
        exact=exact,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    org_id: Union[Unset, int] = UNSET,
    path: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    exact: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[List[FolderOut], None, None, HTTPValidationError]]:
    """Gets a page of all folders the user has access to:
    - If the user is basic, they can only access folders they had rights on.
    - If the user is orgadmin, they can access all of their own organization's folders.

    Additionally, search query parameters can be provided. In case 'path' is provided,
    'name' is ignored. An extra parameter 'exact' can be set if the exact folder path or
    name is needed from the folders."""

    return (
        await asyncio_detailed(
            client=client,
            org_id=org_id,
            path=path,
            name=name,
            exact=exact,
            limit=limit,
            offset=offset,
        )
    ).parsed
