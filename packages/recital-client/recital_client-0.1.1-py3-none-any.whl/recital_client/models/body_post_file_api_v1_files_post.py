from io import BytesIO
from typing import Any, Dict, List

import attr

from ..types import File


@attr.s(auto_attribs=True)
class BodyPostFileApiV1Files_Post:
    """  """

    folder_id: int
    file_in: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folder_id = self.folder_id
        file_in = self.file_in.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folder_id": folder_id,
                "file_in": file_in,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BodyPostFileApiV1Files_Post":
        d = src_dict.copy()
        folder_id = d.pop("folder_id")

        file_in = File(payload=BytesIO(d.pop("file_in")))

        body_post_file_api_v1_files_post = BodyPostFileApiV1Files_Post(
            folder_id=folder_id,
            file_in=file_in,
        )

        body_post_file_api_v1_files_post.additional_properties = d
        return body_post_file_api_v1_files_post

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
