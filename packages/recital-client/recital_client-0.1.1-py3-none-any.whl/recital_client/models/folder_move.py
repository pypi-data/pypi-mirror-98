from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class FolderMove:
    """ Folder schema for move. """

    dst_folder_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dst_folder_id = self.dst_folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dst_folder_id": dst_folder_id,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FolderMove":
        d = src_dict.copy()
        dst_folder_id = d.pop("dst_folder_id")

        folder_move = FolderMove(
            dst_folder_id=dst_folder_id,
        )

        folder_move.additional_properties = d
        return folder_move

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
