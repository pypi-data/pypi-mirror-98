from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.dropdown_option_archive_record import DropdownOptionArchiveRecord
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownOption")


@attr.s(auto_attribs=True)
class DropdownOption:
    """  """

    id: str
    archive_record: Union[Unset, None, DropdownOptionArchiveRecord] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = DropdownOptionArchiveRecord.from_dict(_archive_record)

        name = d.pop("name", UNSET)

        dropdown_option = cls(
            id=id,
            archive_record=archive_record,
            name=name,
        )

        return dropdown_option
