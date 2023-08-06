from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..models.request_task_schema import RequestTaskSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTask")


@attr.s(auto_attribs=True)
class RequestTask:
    """  """

    fields: Fields
    id: str
    sample_group_ids: List[str]
    schema: RequestTaskSchema
    schema_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        sample_group_ids = self.sample_group_ids

        schema = self.schema.to_dict()

        schema_id = self.schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
                "sampleGroupIds": sample_group_ids,
                "schema": schema,
            }
        )
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        sample_group_ids = cast(List[str], d.pop("sampleGroupIds"))

        schema = RequestTaskSchema.from_dict(d.pop("schema"))

        schema_id = d.pop("schemaId", UNSET)

        request_task = cls(
            fields=fields,
            id=id,
            sample_group_ids=sample_group_ids,
            schema=schema,
            schema_id=schema_id,
        )

        return request_task
