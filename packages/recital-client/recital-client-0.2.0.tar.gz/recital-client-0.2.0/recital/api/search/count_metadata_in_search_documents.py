from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.doc_count import DocCount
from ...models.doc_search_metadata_name import DocSearchMetadataName
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: DocSearchMetadataName,
) -> Dict[str, Any]:
    url = "{}/api/v1/search/documents/metadata/count/".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[DocCount, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = DocCount.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 422:
        response_422 = None

        return response_422
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DocCount, None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DocSearchMetadataName,
) -> Response[Union[DocCount, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: DocSearchMetadataName,
) -> Optional[Union[DocCount, None, None, None, None, None]]:
    """Count the documents having a specific metadata in a document result set.
    Only orgadmins can manage metadata in a search result set.
    If no folder_ids are given, by default all folders of the organization are searched."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DocSearchMetadataName,
) -> Response[Union[DocCount, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: DocSearchMetadataName,
) -> Optional[Union[DocCount, None, None, None, None, None]]:
    """Count the documents having a specific metadata in a document result set.
    Only orgadmins can manage metadata in a search result set.
    If no folder_ids are given, by default all folders of the organization are searched."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
