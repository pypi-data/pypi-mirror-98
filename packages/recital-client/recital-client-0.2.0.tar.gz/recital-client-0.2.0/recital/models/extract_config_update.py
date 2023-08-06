from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExtractConfigUpdate")


@attr.s(auto_attribs=True)
class ExtractConfigUpdate:
    """ Extract configuration update schema. """

    n_proposed_paragraphs: int
    n_auto_paragraphs: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        n_proposed_paragraphs = self.n_proposed_paragraphs
        n_auto_paragraphs = self.n_auto_paragraphs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "n_proposed_paragraphs": n_proposed_paragraphs,
                "n_auto_paragraphs": n_auto_paragraphs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        n_proposed_paragraphs = d.pop("n_proposed_paragraphs")

        n_auto_paragraphs = d.pop("n_auto_paragraphs")

        extract_config_update = cls(
            n_proposed_paragraphs=n_proposed_paragraphs,
            n_auto_paragraphs=n_auto_paragraphs,
        )

        extract_config_update.additional_properties = d
        return extract_config_update

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
