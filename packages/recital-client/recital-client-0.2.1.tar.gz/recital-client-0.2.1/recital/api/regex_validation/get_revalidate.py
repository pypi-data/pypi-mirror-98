from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    regex: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/revalidate/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "regex": regex,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, None, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = None

        return response_422
    if response.status_code == 409:
        response_409 = None

        return response_409
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, None, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    regex: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        regex=regex,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    regex: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Validates a regex before running a value extract task.

    Regexes need to be validated because:
    - Not all operators are supported by ES
    (https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html)
    - Of risks of DDoS by regex injection
    (https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)

    Only orgadmins are allowed to validate regexes."""

    return sync_detailed(
        client=client,
        regex=regex,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    regex: str,
) -> Response[Union[None, None, None, None, None]]:
    kwargs = _get_kwargs(
        client=client,
        regex=regex,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    regex: str,
) -> Optional[Union[None, None, None, None, None]]:
    """Validates a regex before running a value extract task.

    Regexes need to be validated because:
    - Not all operators are supported by ES
    (https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html)
    - Of risks of DDoS by regex injection
    (https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)

    Only orgadmins are allowed to validate regexes."""

    return (
        await asyncio_detailed(
            client=client,
            regex=regex,
        )
    ).parsed
