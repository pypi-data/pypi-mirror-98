from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dna_sequence import DnaSequence

T = TypeVar("T", bound="DnaSequencesPaginatedList")


@attr.s(auto_attribs=True)
class DnaSequencesPaginatedList:
    """  """

    next_token: str
    dna_sequences: List[DnaSequence]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        dna_sequences = []
        for dna_sequences_item_data in self.dna_sequences:
            dna_sequences_item = dna_sequences_item_data.to_dict()

            dna_sequences.append(dna_sequences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "dnaSequences": dna_sequences,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        dna_sequences = []
        _dna_sequences = d.pop("dnaSequences")
        for dna_sequences_item_data in _dna_sequences:
            dna_sequences_item = DnaSequence.from_dict(dna_sequences_item_data)

            dna_sequences.append(dna_sequences_item)

        dna_sequences_paginated_list = cls(
            next_token=next_token,
            dna_sequences=dna_sequences,
        )

        return dna_sequences_paginated_list
