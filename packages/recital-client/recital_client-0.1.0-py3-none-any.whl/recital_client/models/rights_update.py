from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class RightsUpdate:
    """ Rights schema to receive from PUT methods. """

    write: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        write = self.write

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "write": write,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "RightsUpdate":
        d = src_dict.copy()
        write = d.pop("write")

        rights_update = RightsUpdate(
            write=write,
        )

        rights_update.additional_properties = d
        return rights_update

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
