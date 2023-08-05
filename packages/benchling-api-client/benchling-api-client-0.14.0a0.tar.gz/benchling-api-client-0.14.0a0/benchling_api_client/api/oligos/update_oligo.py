from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.oligo import Oligo
from ...models.oligo_update import OligoUpdate
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    oligo_id: str,
    json_body: OligoUpdate,
) -> Dict[str, Any]:
    url = "{}/oligos/{oligo_id}".format(client.base_url, oligo_id=oligo_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Oligo, BadRequestError]]:
    if response.status_code == 200:
        response_200 = Oligo.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Oligo, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    oligo_id: str,
    json_body: OligoUpdate,
) -> Response[Union[Oligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    oligo_id: str,
    json_body: OligoUpdate,
) -> Optional[Union[Oligo, BadRequestError]]:
    """ Update an Oligo """

    return sync_detailed(
        client=client,
        oligo_id=oligo_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    oligo_id: str,
    json_body: OligoUpdate,
) -> Response[Union[Oligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    oligo_id: str,
    json_body: OligoUpdate,
) -> Optional[Union[Oligo, BadRequestError]]:
    """ Update an Oligo """

    return (
        await asyncio_detailed(
            client=client,
            oligo_id=oligo_id,
            json_body=json_body,
        )
    ).parsed
