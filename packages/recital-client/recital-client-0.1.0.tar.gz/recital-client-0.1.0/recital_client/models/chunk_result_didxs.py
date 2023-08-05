from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class ChunkResultDidxs:
    """  """

    additional_properties: Dict[str, List[None]] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []

            for additional_property_item_data in prop:
                additional_property_item = None

                field_dict[prop_name].append(additional_property_item)

                field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ChunkResultDidxs":
        d = src_dict.copy()
        chunk_result_didxs = ChunkResultDidxs()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in _additional_property:
                additional_property_item = None

                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        chunk_result_didxs.additional_properties = additional_properties
        return chunk_result_didxs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List[None]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List[None]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
