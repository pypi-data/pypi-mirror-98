from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.indexing_task_out import IndexingTaskOut
from ...models.indexing_task_update import IndexingTaskUpdate
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: int,
    json_body: IndexingTaskUpdate,
) -> Dict[str, Any]:
    url = "{}/api/v1/tasks/indexing/{task_id}/update/".format(client.base_url, task_id=task_id)

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
) -> Optional[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = IndexingTaskOut.from_dict(response.json())

        return response_200
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
) -> Response[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    json_body: IndexingTaskUpdate,
) -> Response[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    task_id: int,
    json_body: IndexingTaskUpdate,
) -> Optional[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    """Update an indexing task by passing a number of processed items.
    This number is added to the number of already processed documents.
    The route automatically sets the task as completed,
    if the total number of documents to process is reached.

    Only services can update indexing reports."""

    return sync_detailed(
        client=client,
        task_id=task_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    json_body: IndexingTaskUpdate,
) -> Response[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: int,
    json_body: IndexingTaskUpdate,
) -> Optional[Union[IndexingTaskOut, None, None, None, HTTPValidationError]]:
    """Update an indexing task by passing a number of processed items.
    This number is added to the number of already processed documents.
    The route automatically sets the task as completed,
    if the total number of documents to process is reached.

    Only services can update indexing reports."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            json_body=json_body,
        )
    ).parsed
