from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.multiple_containers_transfer import MultipleContainersTransfer

T = TypeVar("T", bound="MultipleContainersTransfersList")


@attr.s(auto_attribs=True)
class MultipleContainersTransfersList:
    """  """

    transfers: List[MultipleContainersTransfer]

    def to_dict(self) -> Dict[str, Any]:
        transfers = []
        for transfers_item_data in self.transfers:
            transfers_item = transfers_item_data.to_dict()

            transfers.append(transfers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "transfers": transfers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        transfers = []
        _transfers = d.pop("transfers")
        for transfers_item_data in _transfers:
            transfers_item = MultipleContainersTransfer.from_dict(transfers_item_data)

            transfers.append(transfers_item)

        multiple_containers_transfers_list = cls(
            transfers=transfers,
        )

        return multiple_containers_transfers_list
