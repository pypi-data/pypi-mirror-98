from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    validate: bool,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/import/{metadata_import_id}/validate/".format(
        client.base_url, metadata_import_id=metadata_import_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "validate": validate,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    if response.status_code == 202:
        response_202 = None

        return response_202
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    validate: bool,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
        validate=validate,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    validate: bool,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Validates or cancel a checked metadata import task.

    If validated, the update task is set up and executed.

    Only orgadmins can validate or cancel metadata import tasks."""

    return sync_detailed(
        client=client,
        metadata_import_id=metadata_import_id,
        validate=validate,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    validate: bool,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
        validate=validate,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    validate: bool,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Validates or cancel a checked metadata import task.

    If validated, the update task is set up and executed.

    Only orgadmins can validate or cancel metadata import tasks."""

    return (
        await asyncio_detailed(
            client=client,
            metadata_import_id=metadata_import_id,
            validate=validate,
        )
    ).parsed
