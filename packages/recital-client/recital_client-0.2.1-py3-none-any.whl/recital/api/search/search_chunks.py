from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.search_query_string_query import SearchQueryStringQuery
from ...models.search_result_chunks import SearchResultChunks
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: SearchQueryStringQuery,
    query_id: Union[Unset, int] = UNSET,
    skip_autosuggest: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Dict[str, Any]:
    url = "{}/api/v1/search/chunks/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query_id": query_id,
        "skip_autosuggest": skip_autosuggest,
        "limit": limit,
        "offset": offset,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[SearchResultChunks, None, None, None, None, None]]:
    if response.status_code == 200:
        response_200 = SearchResultChunks.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[SearchResultChunks, None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SearchQueryStringQuery,
    query_id: Union[Unset, int] = UNSET,
    skip_autosuggest: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[SearchResultChunks, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        query_id=query_id,
        skip_autosuggest=skip_autosuggest,
        limit=limit,
        offset=offset,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: SearchQueryStringQuery,
    query_id: Union[Unset, int] = UNSET,
    skip_autosuggest: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[SearchResultChunks, None, None, None, None, None]]:
    """Chunk searching endpoint.

    The route takes as input a query and returns a list of chunks ordered
    by their ranking score.

    The user must have at least read rights on the folders they are searching in.

    If no folder_ids are given, all folders the user has rights on are searched.

    Queries longer than 255 characters are truncated.

    In case the request is another result page of an existing query,
    the query_id parameter must be set to avoid storing the same query several times."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        query_id=query_id,
        skip_autosuggest=skip_autosuggest,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SearchQueryStringQuery,
    query_id: Union[Unset, int] = UNSET,
    skip_autosuggest: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[SearchResultChunks, None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        query_id=query_id,
        skip_autosuggest=skip_autosuggest,
        limit=limit,
        offset=offset,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: SearchQueryStringQuery,
    query_id: Union[Unset, int] = UNSET,
    skip_autosuggest: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[SearchResultChunks, None, None, None, None, None]]:
    """Chunk searching endpoint.

    The route takes as input a query and returns a list of chunks ordered
    by their ranking score.

    The user must have at least read rights on the folders they are searching in.

    If no folder_ids are given, all folders the user has rights on are searched.

    Queries longer than 255 characters are truncated.

    In case the request is another result page of an existing query,
    the query_id parameter must be set to avoid storing the same query several times."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            query_id=query_id,
            skip_autosuggest=skip_autosuggest,
            limit=limit,
            offset=offset,
        )
    ).parsed
