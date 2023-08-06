from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.get_version_styled_html_pages_response_get_version_styled_html_pages_api_v1_files_versions_version_id_styled_html_get import (
    GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_nums: List[int],
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/{version_id}/styled_html/".format(client.base_url, version_id=version_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_page_nums = page_nums

    params: Dict[str, Any] = {
        "page_nums": json_page_nums,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    if response.status_code == 200:
        response_200 = GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet.from_dict(
            response.json()
        )

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
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
) -> Response[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_nums: List[int],
) -> Response[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        page_nums=page_nums,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_nums: List[int],
) -> Optional[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    """Get one page of the html representation of a file version.

    The HTML representation of the version is generated during indexing.

    Consequently, it may be unavailable until indexing is done.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return sync_detailed(
        client=client,
        version_id=version_id,
        page_nums=page_nums,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_nums: List[int],
) -> Response[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        version_id=version_id,
        page_nums=page_nums,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    version_id: int,
    page_nums: List[int],
) -> Optional[
    Union[
        GetVersionStyledHtmlPagesResponseGetVersionStyledHtmlPagesApiV1FilesVersionsVersionIdStyledHtmlGet,
        None,
        None,
        None,
        None,
        HTTPValidationError,
    ]
]:
    """Get one page of the html representation of a file version.

    The HTML representation of the version is generated during indexing.

    Consequently, it may be unavailable until indexing is done.
    - Basic users can only access files in folders they have rights on.
    - Orgadmins can access files in all of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            version_id=version_id,
            page_nums=page_nums,
        )
    ).parsed
