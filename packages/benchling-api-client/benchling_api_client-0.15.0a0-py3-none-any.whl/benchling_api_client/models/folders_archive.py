from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.folders_archive_reason import FoldersArchiveReason

T = TypeVar("T", bound="FoldersArchive")


@attr.s(auto_attribs=True)
class FoldersArchive:
    """  """

    folder_ids: List[str]
    reason: FoldersArchiveReason

    def to_dict(self) -> Dict[str, Any]:
        folder_ids = self.folder_ids

        reason = self.reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "folderIds": folder_ids,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_ids = cast(List[str], d.pop("folderIds"))

        reason = FoldersArchiveReason(d.pop("reason"))

        folders_archive = cls(
            folder_ids=folder_ids,
            reason=reason,
        )

        return folders_archive
