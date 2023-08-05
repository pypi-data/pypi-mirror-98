from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="MultipleContainersTransferSourceConcentration")


@attr.s(auto_attribs=True)
class MultipleContainersTransferSourceConcentration:
    """Concentration at which to transfer entities or batches. Not applicable for container-to-container transfers (the concentration of the source container’s contents will be used)."""

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        multiple_containers_transfer_source_concentration = cls()

        multiple_containers_transfer_source_concentration.additional_properties = d
        return multiple_containers_transfer_source_concentration

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
