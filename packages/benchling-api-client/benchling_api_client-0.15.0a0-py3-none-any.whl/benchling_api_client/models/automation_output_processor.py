from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.archive_record import ArchiveRecord
from ..models.automation_file_automation_file_config import AutomationFileAutomationFileConfig
from ..models.automation_file_file import AutomationFileFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessor")


@attr.s(auto_attribs=True)
class AutomationOutputProcessor:
    """  """

    id: str
    api_url: Union[Unset, str] = UNSET
    archive_record: Union[Unset, ArchiveRecord] = UNSET
    assay_run_id: Union[Unset, str] = UNSET
    automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
    file: Union[Unset, None, AutomationFileFile] = UNSET
    status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        api_url = self.api_url
        archive_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict()

        assay_run_id = self.assay_run_id
        automation_file_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.automation_file_config, Unset):
            automation_file_config = self.automation_file_config.to_dict()

        file: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict() if self.file else None

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if automation_file_config is not UNSET:
            field_dict["automationFileConfig"] = automation_file_config
        if file is not UNSET:
            field_dict["file"] = file
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        api_url = d.pop("apiURL", UNSET)

        archive_record: Union[Unset, ArchiveRecord] = UNSET
        _archive_record = d.pop("archiveRecord", UNSET)
        if not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(_archive_record)

        assay_run_id = d.pop("assayRunId", UNSET)

        automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
        _automation_file_config = d.pop("automationFileConfig", UNSET)
        if not isinstance(_automation_file_config, Unset):
            automation_file_config = AutomationFileAutomationFileConfig.from_dict(_automation_file_config)

        file = None
        _file = d.pop("file", UNSET)
        if _file is not None and not isinstance(_file, Unset):
            file = AutomationFileFile.from_dict(_file)

        status = d.pop("status", UNSET)

        automation_output_processor = cls(
            id=id,
            api_url=api_url,
            archive_record=archive_record,
            assay_run_id=assay_run_id,
            automation_file_config=automation_file_config,
            file=file,
            status=status,
        )

        return automation_output_processor
