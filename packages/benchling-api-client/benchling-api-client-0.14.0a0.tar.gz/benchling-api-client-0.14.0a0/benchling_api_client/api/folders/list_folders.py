from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.folders_paginated_list import FoldersPaginatedList
from ...models.list_folders_sort import ListFoldersSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
    sort: Union[Unset, None, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    parent_folder_id: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/folders".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, None, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value if sort else None

    params: Dict[str, Any] = {}
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if not isinstance(name_includes, Unset) and name_includes is not None:
        params["nameIncludes"] = name_includes
    if not isinstance(parent_folder_id, Unset) and parent_folder_id is not None:
        params["parentFolderId"] = parent_folder_id
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[FoldersPaginatedList]:
    if response.status_code == 200:
        response_200 = FoldersPaginatedList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[FoldersPaginatedList]:
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
    sort: Union[Unset, None, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    parent_folder_id: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Response[FoldersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
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
    sort: Union[Unset, None, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    parent_folder_id: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Optional[FoldersPaginatedList]:
    """  """

    return sync_detailed(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
    sort: Union[Unset, None, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    parent_folder_id: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Response[FoldersPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        next_token=next_token,
        page_size=page_size,
        sort=sort,
        archive_reason=archive_reason,
        name_includes=name_includes,
        parent_folder_id=parent_folder_id,
        project_id=project_id,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    next_token: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = 50,
    sort: Union[Unset, None, ListFoldersSort] = ListFoldersSort.NAME,
    archive_reason: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    parent_folder_id: Union[Unset, None, str] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
) -> Optional[FoldersPaginatedList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            next_token=next_token,
            page_size=page_size,
            sort=sort,
            archive_reason=archive_reason,
            name_includes=name_includes,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
            ids=ids,
        )
    ).parsed
