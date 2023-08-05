from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunUpdate")


@attr.s(auto_attribs=True)
class AssayRunUpdate:
    """  """

    fields: Union[Unset, Fields] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        assay_run_update = cls(
            fields=fields,
        )

        return assay_run_update
