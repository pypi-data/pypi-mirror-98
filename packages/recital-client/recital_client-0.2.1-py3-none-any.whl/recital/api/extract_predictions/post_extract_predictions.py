from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.extract_prediction_in import ExtractPredictionIn
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: ExtractPredictionIn,
    task_id: int,
    doc_id: int,
) -> Dict[str, Any]:
    url = "{}/api/v1/extract/predictions/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "task_id": task_id,
        "doc_id": doc_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, None, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = None

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, None, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractPredictionIn,
    task_id: int,
    doc_id: int,
) -> Response[Union[None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        task_id=task_id,
        doc_id=doc_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ExtractPredictionIn,
    task_id: int,
    doc_id: int,
) -> Optional[Union[None, None, None, HTTPValidationError]]:
    """Stores the predictions for a document.

    Only services are allowed to post predictions.

    The document is identified by both the task id and the doc id query parameters.

    The prediction status must be either:
    - pred, if the prediction is done for a paragraph or question task in manual mode
    - auto, if the prediction is done for a value, question or paragraph task in auto mode"""

    return sync_detailed(
        client=client,
        json_body=json_body,
        task_id=task_id,
        doc_id=doc_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ExtractPredictionIn,
    task_id: int,
    doc_id: int,
) -> Response[Union[None, None, None, HTTPValidationError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        task_id=task_id,
        doc_id=doc_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ExtractPredictionIn,
    task_id: int,
    doc_id: int,
) -> Optional[Union[None, None, None, HTTPValidationError]]:
    """Stores the predictions for a document.

    Only services are allowed to post predictions.

    The document is identified by both the task id and the doc id query parameters.

    The prediction status must be either:
    - pred, if the prediction is done for a paragraph or question task in manual mode
    - auto, if the prediction is done for a value, question or paragraph task in auto mode"""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            task_id=task_id,
            doc_id=doc_id,
        )
    ).parsed
