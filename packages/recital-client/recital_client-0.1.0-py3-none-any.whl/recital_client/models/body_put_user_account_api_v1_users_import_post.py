from io import BytesIO
from typing import Any, Dict, List

import attr

from ..types import File


@attr.s(auto_attribs=True)
class BodyPutUserAccountApiV1UsersImport_Post:
    """  """

    excel: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        excel = self.excel.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "excel": excel,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BodyPutUserAccountApiV1UsersImport_Post":
        d = src_dict.copy()
        excel = File(payload=BytesIO(d.pop("excel")))

        body_put_user_account_api_v1_users_import_post = BodyPutUserAccountApiV1UsersImport_Post(
            excel=excel,
        )

        body_put_user_account_api_v1_users_import_post.additional_properties = d
        return body_put_user_account_api_v1_users_import_post

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
