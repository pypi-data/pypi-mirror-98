from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.body_create_file_api_v1_files_post import BodyCreateFileApiV1Files_Post
from ...models.file_item_out_with_latest_version import FileItemOutWithLatestVersion
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyCreateFileApiV1Files_Post,
    filename: Union[Unset, str] = UNSET,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "filename": filename,
        "idx_task_id": idx_task_id,
        "incremental": incremental,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_data.to_dict(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = FileItemOutWithLatestVersion.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 409:
        response_409 = None

        return response_409
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyCreateFileApiV1Files_Post,
    filename: Union[Unset, str] = UNSET,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
) -> Response[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        filename=filename,
        idx_task_id=idx_task_id,
        incremental=incremental,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyCreateFileApiV1Files_Post,
    filename: Union[Unset, str] = UNSET,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
) -> Optional[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    """Creates a new file item.

    If no file item with same name is in the folder,
    the route creates a new file item and its first version.<br>
    If a file item with same name already exists in the folder,
    the organization versioning policy is applied:
    - If the hash of the uploaded file is the same as the last version,
    nothing is done.
    - If versioning is disabled, the previous item version is deleted,
    and the uploaded one replaces it.
    - If versioning is enabled, a new item version is created.

    If current number of versions exceeds the maximum number defined in the policy,
    the oldest version is deleted.

    An optional idx_task_id query parameter may be passed to the route,
    which will be saved on the file.

    An incremental query parameter could be passed
    to specify if the task item number should be incremented.

    - Basic users can only add files in folders they has write rights on.
    - Orgadmins can add files in any of their organization's folders.
    - Services can also add files within their organization."""

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        filename=filename,
        idx_task_id=idx_task_id,
        incremental=incremental,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyCreateFileApiV1Files_Post,
    filename: Union[Unset, str] = UNSET,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
) -> Response[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        filename=filename,
        idx_task_id=idx_task_id,
        incremental=incremental,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyCreateFileApiV1Files_Post,
    filename: Union[Unset, str] = UNSET,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
) -> Optional[Union[FileItemOutWithLatestVersion, None, None, None, None, None, HTTPValidationError]]:
    """Creates a new file item.

    If no file item with same name is in the folder,
    the route creates a new file item and its first version.<br>
    If a file item with same name already exists in the folder,
    the organization versioning policy is applied:
    - If the hash of the uploaded file is the same as the last version,
    nothing is done.
    - If versioning is disabled, the previous item version is deleted,
    and the uploaded one replaces it.
    - If versioning is enabled, a new item version is created.

    If current number of versions exceeds the maximum number defined in the policy,
    the oldest version is deleted.

    An optional idx_task_id query parameter may be passed to the route,
    which will be saved on the file.

    An incremental query parameter could be passed
    to specify if the task item number should be incremented.

    - Basic users can only add files in folders they has write rights on.
    - Orgadmins can add files in any of their organization's folders.
    - Services can also add files within their organization."""

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            filename=filename,
            idx_task_id=idx_task_id,
            incremental=incremental,
        )
    ).parsed
