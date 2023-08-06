from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_tasks_bulk_create import RequestTasksBulkCreate

T = TypeVar("T", bound="RequestsTasksBulkCreateRequest")


@attr.s(auto_attribs=True)
class RequestsTasksBulkCreateRequest:
    """  """

    tasks: List[RequestTasksBulkCreate]

    def to_dict(self) -> Dict[str, Any]:
        tasks = []
        for tasks_item_data in self.tasks:
            tasks_item = tasks_item_data.to_dict()

            tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tasks": tasks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tasks = []
        _tasks = d.pop("tasks")
        for tasks_item_data in _tasks:
            tasks_item = RequestTasksBulkCreate.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        requests_tasks_bulk_create_request = cls(
            tasks=tasks,
        )

        return requests_tasks_bulk_create_request
