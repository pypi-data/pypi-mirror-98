from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExtractResultValidateIn")


@attr.s(auto_attribs=True)
class ExtractResultValidateIn:
    """ Extract result schema for validate input. """

    validated_rank: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        validated_rank = self.validated_rank

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "validated_rank": validated_rank,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        validated_rank = d.pop("validated_rank")

        extract_result_validate_in = cls(
            validated_rank=validated_rank,
        )

        extract_result_validate_in.additional_properties = d
        return extract_result_validate_in

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
