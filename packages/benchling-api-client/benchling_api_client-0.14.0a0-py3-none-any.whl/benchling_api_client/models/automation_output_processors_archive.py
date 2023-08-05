from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessorsArchive")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorsArchive:
    """  """

    automation_output_processor_ids: List[str]
    reason: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processor_ids = self.automation_output_processor_ids

        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "automationOutputProcessorIds": automation_output_processor_ids,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_output_processor_ids = cast(List[str], d.pop("automationOutputProcessorIds"))

        reason = d.pop("reason", UNSET)

        automation_output_processors_archive = cls(
            automation_output_processor_ids=automation_output_processor_ids,
            reason=reason,
        )

        return automation_output_processors_archive
