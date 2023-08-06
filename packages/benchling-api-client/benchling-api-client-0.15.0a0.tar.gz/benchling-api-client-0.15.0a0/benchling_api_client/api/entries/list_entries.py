from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.entries_paginated_list import EntriesPaginatedList
from ...models.list_entries_review_status import ListEntriesReviewStatus
from ...models.list_entries_sort import ListEntriesSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    review_status: Union[Unset, None, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/entries".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, None, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value if sort else None

    json_review_status: Union[Unset, None, int] = UNSET
    if not isinstance(review_status, Unset):
        json_review_status = review_status.value if review_status else None

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(modified_at, Unset) and modified_at is not None:
        params["modifiedAt"] = modified_at
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if not isinstance(json_review_status, Unset) and json_review_status is not None:
        params["reviewStatus"] = json_review_status
    if not isinstance(mentioned_in, Unset) and mentioned_in is not None:
        params["mentionedIn"] = mentioned_in
    if not isinstance(mentions, Unset) and mentions is not None:
        params["mentions"] = mentions
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = EntriesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    review_status: Union[Unset, None, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    review_status: Union[Unset, None, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    review_status: Union[Unset, None, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Response[Union[EntriesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListEntriesSort] = ListEntriesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    review_status: Union[Unset, None, ListEntriesReviewStatus] = UNSET,
    mentioned_in: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Optional[Union[EntriesPaginatedList, BadRequestError]]:
    """ List notebook entries """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            project_id=project_id,
            archive_reason=archive_reason,
            review_status=review_status,
            mentioned_in=mentioned_in,
            mentions=mentions,
            ids=ids,
        )
    ).parsed
