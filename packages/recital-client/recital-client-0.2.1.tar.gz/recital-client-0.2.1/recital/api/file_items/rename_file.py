from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.file_item_out import FileItemOut
from ...models.file_item_rename import FileItemRename
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    file_id: int,
    json_body: FileItemRename,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/{file_id}/rename/".format(client.base_url, file_id=file_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[FileItemOut, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = FileItemOut.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 409:
        response_409 = None

        return response_409
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = None

        return response_422
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[FileItemOut, None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    file_id: int,
    json_body: FileItemRename,
) -> Response[Union[FileItemOut, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    file_id: int,
    json_body: FileItemRename,
) -> Optional[Union[FileItemOut, None, None, None, None, None]]:
    """Rename a file item.

    Modifies the display name of the file.

    The changes are also applied to all of the file item's versions.
    - Basic users can only update files in folders they has write rights on.
    - Orgadmins can update files in any of their organization's folders."""

    return sync_detailed(
        client=client,
        file_id=file_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    file_id: int,
    json_body: FileItemRename,
) -> Response[Union[FileItemOut, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    file_id: int,
    json_body: FileItemRename,
) -> Optional[Union[FileItemOut, None, None, None, None, None]]:
    """Rename a file item.

    Modifies the display name of the file.

    The changes are also applied to all of the file item's versions.
    - Basic users can only update files in folders they has write rights on.
    - Orgadmins can update files in any of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            file_id=file_id,
            json_body=json_body,
        )
    ).parsed
