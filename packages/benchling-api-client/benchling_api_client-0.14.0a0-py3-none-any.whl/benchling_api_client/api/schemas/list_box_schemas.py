from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.box_schemas_paginated_list import BoxSchemasPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
) -> Dict[str, Any]:
    url = "{}/box-schemas".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BoxSchemasPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = BoxSchemasPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BoxSchemasPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
) -> Response[Union[BoxSchemasPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
) -> Optional[Union[BoxSchemasPaginatedList, BadRequestError]]:
    """ List box schemas """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
) -> Response[Union[BoxSchemasPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
) -> Optional[Union[BoxSchemasPaginatedList, BadRequestError]]:
    """ List box schemas """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
        )
    ).parsed
