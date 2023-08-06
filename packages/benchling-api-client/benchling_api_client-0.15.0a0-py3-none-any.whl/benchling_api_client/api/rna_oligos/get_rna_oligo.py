from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.rna_oligo import RnaOligo
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    oligo_id: str,
) -> Dict[str, Any]:
    url = "{}/rna-oligos/{oligo_id}".format(client.base_url, oligo_id=oligo_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[RnaOligo, BadRequestError]]:
    if response.status_code == 200:
        response_200 = RnaOligo.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RnaOligo, BadRequestError]]:
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
) -> Response[Union[RnaOligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    oligo_id: str,
) -> Optional[Union[RnaOligo, BadRequestError]]:
    """ Get an RNA Oligo """

    return sync_detailed(
        client=client,
        oligo_id=oligo_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    oligo_id: str,
) -> Response[Union[RnaOligo, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        oligo_id=oligo_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    oligo_id: str,
) -> Optional[Union[RnaOligo, BadRequestError]]:
    """ Get an RNA Oligo """

    return (
        await asyncio_detailed(
            client=client,
            oligo_id=oligo_id,
        )
    ).parsed
