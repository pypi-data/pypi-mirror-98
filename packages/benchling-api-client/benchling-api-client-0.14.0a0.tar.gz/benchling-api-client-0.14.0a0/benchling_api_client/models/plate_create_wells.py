from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.plate_create_wells_additional_property import PlateCreateWellsAdditionalProperty

T = TypeVar("T", bound="PlateCreateWells")


@attr.s(auto_attribs=True)
class PlateCreateWells:
    """  """

    additional_properties: Dict[str, PlateCreateWellsAdditionalProperty] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plate_create_wells = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = PlateCreateWellsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        plate_create_wells.additional_properties = additional_properties
        return plate_create_wells

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> PlateCreateWellsAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: PlateCreateWellsAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
