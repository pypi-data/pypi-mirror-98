from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.custom_entity_bulk_create import CustomEntityBulkCreate

T = TypeVar("T", bound="CustomEntitiesBulkCreateRequest")


@attr.s(auto_attribs=True)
class CustomEntitiesBulkCreateRequest:
    """  """

    custom_entities: List[CustomEntityBulkCreate]

    def to_dict(self) -> Dict[str, Any]:
        custom_entities = []
        for custom_entities_item_data in self.custom_entities:
            custom_entities_item = custom_entities_item_data.to_dict()

            custom_entities.append(custom_entities_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "customEntities": custom_entities,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_entities = []
        _custom_entities = d.pop("customEntities")
        for custom_entities_item_data in _custom_entities:
            custom_entities_item = CustomEntityBulkCreate.from_dict(custom_entities_item_data)

            custom_entities.append(custom_entities_item)

        custom_entities_bulk_create_request = cls(
            custom_entities=custom_entities,
        )

        return custom_entities_bulk_create_request
