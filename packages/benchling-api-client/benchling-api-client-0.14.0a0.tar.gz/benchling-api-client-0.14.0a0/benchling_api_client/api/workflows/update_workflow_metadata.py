from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.workflow import Workflow
from ...models.workflow_patch import WorkflowPatch
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    workflow_id: str,
    json_body: WorkflowPatch,
) -> Dict[str, Any]:
    url = "{}/workflows/{workflow_id}".format(client.base_url, workflow_id=workflow_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Workflow]:
    if response.status_code == 200:
        response_200 = Workflow.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Workflow]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    workflow_id: str,
    json_body: WorkflowPatch,
) -> Response[Workflow]:
    kwargs = _get_kwargs(
        client=client,
        workflow_id=workflow_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    workflow_id: str,
    json_body: WorkflowPatch,
) -> Optional[Workflow]:
    """ Update workflow metadata """

    return sync_detailed(
        client=client,
        workflow_id=workflow_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    workflow_id: str,
    json_body: WorkflowPatch,
) -> Response[Workflow]:
    kwargs = _get_kwargs(
        client=client,
        workflow_id=workflow_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    workflow_id: str,
    json_body: WorkflowPatch,
) -> Optional[Workflow]:
    """ Update workflow metadata """

    return (
        await asyncio_detailed(
            client=client,
            workflow_id=workflow_id,
            json_body=json_body,
        )
    ).parsed
