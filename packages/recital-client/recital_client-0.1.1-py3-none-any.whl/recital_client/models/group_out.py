from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class GroupOut:
    """ Group schema to output from GET methods. """

    name: str
    id: int
    org_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        org_id = self.org_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "org_id": org_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "GroupOut":
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id")

        org_id = d.pop("org_id")

        group_out = GroupOut(
            name=name,
            id=id,
            org_id=org_id,
        )

        group_out.additional_properties = d
        return group_out

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
