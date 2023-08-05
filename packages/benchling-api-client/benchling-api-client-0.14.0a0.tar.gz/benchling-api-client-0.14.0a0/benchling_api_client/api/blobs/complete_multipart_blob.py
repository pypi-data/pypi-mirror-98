from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.blob import Blob
from ...models.blob_complete import BlobComplete
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    blob_id: str,
    json_body: BlobComplete,
) -> Dict[str, Any]:
    url = "{}/blobs/{blob_id}:complete-upload".format(client.base_url, blob_id=blob_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Blob, BadRequestError]]:
    if response.status_code == 200:
        response_200 = Blob.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Blob, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    blob_id: str,
    json_body: BlobComplete,
) -> Response[Union[Blob, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    blob_id: str,
    json_body: BlobComplete,
) -> Optional[Union[Blob, BadRequestError]]:
    """ Combine blob parts into a single blob. """

    return sync_detailed(
        client=client,
        blob_id=blob_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    blob_id: str,
    json_body: BlobComplete,
) -> Response[Union[Blob, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    blob_id: str,
    json_body: BlobComplete,
) -> Optional[Union[Blob, BadRequestError]]:
    """ Combine blob parts into a single blob. """

    return (
        await asyncio_detailed(
            client=client,
            blob_id=blob_id,
            json_body=json_body,
        )
    ).parsed
