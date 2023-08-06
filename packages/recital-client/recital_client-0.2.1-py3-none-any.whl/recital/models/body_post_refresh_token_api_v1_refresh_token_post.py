from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyPostRefreshTokenApiV1RefreshToken_Post")


@attr.s(auto_attribs=True)
class BodyPostRefreshTokenApiV1RefreshToken_Post:
    """  """

    refresh_token: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        refresh_token = self.refresh_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "refresh_token": refresh_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        refresh_token = d.pop("refresh_token")

        body_post_refresh_token_api_v1_refresh_token_post = cls(
            refresh_token=refresh_token,
        )

        body_post_refresh_token_api_v1_refresh_token_post.additional_properties = d
        return body_post_refresh_token_api_v1_refresh_token_post

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
