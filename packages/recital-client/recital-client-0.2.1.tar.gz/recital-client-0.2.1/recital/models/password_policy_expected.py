from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PasswordPolicyExpected")


@attr.s(auto_attribs=True)
class PasswordPolicyExpected:
    """Policy schema that represents the expected password policy
    for login endpoint."""

    min_length: int
    digit: bool
    upper: bool
    lower: bool
    special: bool
    max_similarity: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        min_length = self.min_length
        digit = self.digit
        upper = self.upper
        lower = self.lower
        special = self.special
        max_similarity = self.max_similarity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min_length": min_length,
                "digit": digit,
                "upper": upper,
                "lower": lower,
                "special": special,
                "max_similarity": max_similarity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        min_length = d.pop("min_length")

        digit = d.pop("digit")

        upper = d.pop("upper")

        lower = d.pop("lower")

        special = d.pop("special")

        max_similarity = d.pop("max_similarity")

        password_policy_expected = cls(
            min_length=min_length,
            digit=digit,
            upper=upper,
            lower=lower,
            special=special,
            max_similarity=max_similarity,
        )

        password_policy_expected.additional_properties = d
        return password_policy_expected

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
