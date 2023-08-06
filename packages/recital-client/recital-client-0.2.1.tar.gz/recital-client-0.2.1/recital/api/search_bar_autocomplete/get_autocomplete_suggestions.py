from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: str,
    suggestions: Union[Unset, int] = 10,
) -> Dict[str, Any]:
    url = "{}/api/v1/search/autocomplete/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
        "suggestions": suggestions,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[str], None, None, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(List[str], response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[str], None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    suggestions: Union[Unset, int] = 10,
) -> Response[Union[List[str], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        suggestions=suggestions,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: str,
    suggestions: Union[Unset, int] = 10,
) -> Optional[Union[List[str], None, None, HTTPValidationError]]:
    """Suggest queries from past ones.

    The route only looks in the user's history.

    If suggestions is specified, the route returns this number of suggestions,
    otherwise the default number of returned suggestions is 10."""

    return sync_detailed(
        client=client,
        query=query,
        suggestions=suggestions,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    suggestions: Union[Unset, int] = 10,
) -> Response[Union[List[str], None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        suggestions=suggestions,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str,
    suggestions: Union[Unset, int] = 10,
) -> Optional[Union[List[str], None, None, HTTPValidationError]]:
    """Suggest queries from past ones.

    The route only looks in the user's history.

    If suggestions is specified, the route returns this number of suggestions,
    otherwise the default number of returned suggestions is 10."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            suggestions=suggestions,
        )
    ).parsed
