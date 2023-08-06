from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.body_post_metadata_import_api_v1_metadata_import_post import (
    BodyPostMetadataImportApiV1MetadataImport_Post,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.metadata_import_create_out import MetadataImportCreateOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyPostMetadataImportApiV1MetadataImport_Post,
    org_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/import/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "org_id": org_id,
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
) -> Optional[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    if response.status_code == 202:
        response_202 = MetadataImportCreateOut.from_dict(response.json())

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


def _build_response(
    *, response: httpx.Response
) -> Response[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyPostMetadataImportApiV1MetadataImport_Post,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        org_id=org_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyPostMetadataImportApiV1MetadataImport_Post,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    """Requests a metadata import tasks. Only orgadmins are allowed to run metadata import.

    The id of the organization is guessed from the session token.

    Only one import at a time per organization is allowed."""

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        org_id=org_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyPostMetadataImportApiV1MetadataImport_Post,
    org_id: Union[Unset, int] = UNSET,
) -> Response[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        org_id=org_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    multipart_data: BodyPostMetadataImportApiV1MetadataImport_Post,
    org_id: Union[Unset, int] = UNSET,
) -> Optional[Union[MetadataImportCreateOut, None, None, None, HTTPValidationError]]:
    """Requests a metadata import tasks. Only orgadmins are allowed to run metadata import.

    The id of the organization is guessed from the session token.

    Only one import at a time per organization is allowed."""

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            org_id=org_id,
        )
    ).parsed
