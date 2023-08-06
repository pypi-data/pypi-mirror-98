from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: int,
    delete_task: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/tasks/{task_id}/cancel/".format(client.base_url, task_id=task_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "delete_task": delete_task,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None, HTTPValidationError]]:
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
    delete_task: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        delete_task=delete_task,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    task_id: int,
    delete_task: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None, None, HTTPValidationError]]:
    """Cancel an extract task.

    Only orgadmins are allowed to cancel extract tasks.

    If the task is in automatic mode and isn't deleted, it goes back in manual mode."""

    return sync_detailed(
        client=client,
        task_id=task_id,
        delete_task=delete_task,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    task_id: int,
    delete_task: Union[Unset, bool] = False,
) -> Response[Union[None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
        delete_task=delete_task,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: int,
    delete_task: Union[Unset, bool] = False,
) -> Optional[Union[None, None, None, None, None, HTTPValidationError]]:
    """Cancel an extract task.

    Only orgadmins are allowed to cancel extract tasks.

    If the task is in automatic mode and isn't deleted, it goes back in manual mode."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
            delete_task=delete_task,
        )
    ).parsed
