from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.well_volume_units import WellVolumeUnits
from ..types import UNSET, Unset

T = TypeVar("T", bound="WellVolume")


@attr.s(auto_attribs=True)
class WellVolume:
    """ Volume of well's contents """

    units: Union[Unset, WellVolumeUnits] = UNSET
    value: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        units: Union[Unset, int] = UNSET
        if not isinstance(self.units, Unset):
            units = self.units.value

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if units is not UNSET:
            field_dict["units"] = units
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        units = None
        _units = d.pop("units", UNSET)
        if _units is not None and _units is not UNSET:
            units = WellVolumeUnits(_units)

        value = d.pop("value", UNSET)

        well_volume = cls(
            units=units,
            value=value,
        )

        well_volume.additional_properties = d
        return well_volume

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
