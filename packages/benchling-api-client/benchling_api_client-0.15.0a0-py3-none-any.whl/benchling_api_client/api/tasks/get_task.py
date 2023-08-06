from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.async_task import AsyncTask
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    task_id: str,
) -> Dict[str, Any]:
    url = "{}/tasks/{task_id}".format(client.base_url, task_id=task_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AsyncTask, NotFoundError]]:
    if response.status_code == 200:
        response_200 = AsyncTask.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AsyncTask, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    task_id: str,
) -> Response[Union[AsyncTask, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    task_id: str,
) -> Optional[Union[AsyncTask, NotFoundError]]:
    """ Get a task by id """

    return sync_detailed(
        client=client,
        task_id=task_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    task_id: str,
) -> Response[Union[AsyncTask, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    task_id: str,
) -> Optional[Union[AsyncTask, NotFoundError]]:
    """ Get a task by id """

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
        )
    ).parsed
