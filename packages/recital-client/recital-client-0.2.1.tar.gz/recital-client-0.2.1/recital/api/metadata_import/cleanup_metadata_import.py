from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.metadata_import_cleanup import MetadataImportCleanup
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    json_body: MetadataImportCleanup,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/import/{metadata_import_id}/finish/".format(
        client.base_url, metadata_import_id=metadata_import_id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
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
    json_body: MetadataImportCleanup,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    json_body: MetadataImportCleanup,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Set a metadata import task as finished.

    This endpoint needs to be called to clean the resources created during import.

    Only services can set a metadata import tasks as finished"""

    return sync_detailed(
        client=client,
        metadata_import_id=metadata_import_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    json_body: MetadataImportCleanup,
) -> Response[Union[None, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        metadata_import_id=metadata_import_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    metadata_import_id: int,
    json_body: MetadataImportCleanup,
) -> Optional[Union[None, None, None, None, HTTPValidationError]]:
    """Set a metadata import task as finished.

    This endpoint needs to be called to clean the resources created during import.

    Only services can set a metadata import tasks as finished"""

    return (
        await asyncio_detailed(
            client=client,
            metadata_import_id=metadata_import_id,
            json_body=json_body,
        )
    ).parsed
