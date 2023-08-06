from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_task_create import ExtractTaskCreate
from ...models.extract_task_out import ExtractTaskOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ExtractTaskCreate,
    model_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/tasks/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "model_id": model_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ExtractTaskOut.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 409:
        response_409 = None

        return response_409
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractTaskCreate,
    model_id: Union[Unset, int] = UNSET,
) -> Response[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        model_id=model_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ExtractTaskCreate,
    model_id: Union[Unset, int] = UNSET,
) -> Optional[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    """Create and run an extract task.

    Only orgadmins are allowed to create and run extract tasks.
    The id of the organization is inferred from the session token.

    Please note that if it's a value extract, the regex must be valid
    (see dedicated endpoint).

    If model id is passed in the parameters, the task is created from the models.
    Otherwise, the model to be created must be passed in the body."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        model_id=model_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractTaskCreate,
    model_id: Union[Unset, int] = UNSET,
) -> Response[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        model_id=model_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ExtractTaskCreate,
    model_id: Union[Unset, int] = UNSET,
) -> Optional[Union[ExtractTaskOut, None, None, None, None, None, HTTPValidationError]]:
    """Create and run an extract task.

    Only orgadmins are allowed to create and run extract tasks.
    The id of the organization is inferred from the session token.

    Please note that if it's a value extract, the regex must be valid
    (see dedicated endpoint).

    If model id is passed in the parameters, the task is created from the models.
    Otherwise, the model to be created must be passed in the body."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            model_id=model_id,
        )
    ).parsed
