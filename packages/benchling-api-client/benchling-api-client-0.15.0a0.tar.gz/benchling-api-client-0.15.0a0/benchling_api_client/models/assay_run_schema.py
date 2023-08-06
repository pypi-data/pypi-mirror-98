from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.assay_run_schema_archive_record import AssayRunSchemaArchiveRecord
from ..models.assay_run_schema_automation_input_file_configs_item import AssayRunSchemaAutomationInputFileConfigsItem
from ..models.assay_run_schema_automation_output_file_configs_item import AssayRunSchemaAutomationOutputFileConfigsItem
from ..models.assay_run_schema_organization import AssayRunSchemaOrganization
from ..models.assay_run_schema_type import AssayRunSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunSchema")


@attr.s(auto_attribs=True)
class AssayRunSchema:
    """  """

    id: str
    archive_record: Union[Unset, None, AssayRunSchemaArchiveRecord] = UNSET
    automation_input_file_configs: Union[Unset, List[AssayRunSchemaAutomationInputFileConfigsItem]] = UNSET
    automation_output_file_configs: Union[Unset, List[AssayRunSchemaAutomationOutputFileConfigsItem]] = UNSET
    derived_from: Union[Unset, None, str] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    name: Union[Unset, str] = UNSET
    organization: Union[Unset, AssayRunSchemaOrganization] = UNSET
    system_name: Union[Unset, str] = UNSET
    type: Union[Unset, AssayRunSchemaType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        automation_input_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_input_file_configs, Unset):
            automation_input_file_configs = []
            for automation_input_file_configs_item_data in self.automation_input_file_configs:
                automation_input_file_configs_item = automation_input_file_configs_item_data.to_dict()

                automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_output_file_configs, Unset):
            automation_output_file_configs = []
            for automation_output_file_configs_item_data in self.automation_output_file_configs:
                automation_output_file_configs_item = automation_output_file_configs_item_data.to_dict()

                automation_output_file_configs.append(automation_output_file_configs_item)

        derived_from = self.derived_from
        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        name = self.name
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        system_name = self.system_name
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if automation_input_file_configs is not UNSET:
            field_dict["automationInputFileConfigs"] = automation_input_file_configs
        if automation_output_file_configs is not UNSET:
            field_dict["automationOutputFileConfigs"] = automation_output_file_configs
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if name is not UNSET:
            field_dict["name"] = name
        if organization is not UNSET:
            field_dict["organization"] = organization
        if system_name is not UNSET:
            field_dict["systemName"] = system_name
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = AssayRunSchemaArchiveRecord.from_dict(_archive_record)

        automation_input_file_configs = []
        _automation_input_file_configs = d.pop("automationInputFileConfigs", UNSET)
        for automation_input_file_configs_item_data in _automation_input_file_configs or []:
            automation_input_file_configs_item = AssayRunSchemaAutomationInputFileConfigsItem.from_dict(
                automation_input_file_configs_item_data
            )

            automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs = []
        _automation_output_file_configs = d.pop("automationOutputFileConfigs", UNSET)
        for automation_output_file_configs_item_data in _automation_output_file_configs or []:
            automation_output_file_configs_item = AssayRunSchemaAutomationOutputFileConfigsItem.from_dict(
                automation_output_file_configs_item_data
            )

            automation_output_file_configs.append(automation_output_file_configs_item)

        derived_from = d.pop("derivedFrom", UNSET)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        name = d.pop("name", UNSET)

        organization: Union[Unset, AssayRunSchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if not isinstance(_organization, Unset):
            organization = AssayRunSchemaOrganization.from_dict(_organization)

        system_name = d.pop("systemName", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = AssayRunSchemaType(_type)

        assay_run_schema = cls(
            id=id,
            archive_record=archive_record,
            automation_input_file_configs=automation_input_file_configs,
            automation_output_file_configs=automation_output_file_configs,
            derived_from=derived_from,
            field_definitions=field_definitions,
            name=name,
            organization=organization,
            system_name=system_name,
            type=type,
        )

        return assay_run_schema
