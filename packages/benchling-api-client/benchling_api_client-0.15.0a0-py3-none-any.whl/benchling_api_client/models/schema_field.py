from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaField")


@attr.s(auto_attribs=True)
class SchemaField:
    """  """

    id: Union[Unset, str] = UNSET
    is_required: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        is_required = self.is_required
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        is_required = d.pop("isRequired", UNSET)

        name = d.pop("name", UNSET)

        schema_field = cls(
            id=id,
            is_required=is_required,
            name=name,
        )

        return schema_field
