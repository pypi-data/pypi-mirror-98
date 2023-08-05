from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class LanguageEntitiesOut:
    """ Entity Types per Language schema for the GET route. """

    lang: str
    entity_types: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lang = self.lang
        entity_types = self.entity_types

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lang": lang,
                "entity_types": entity_types,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "LanguageEntitiesOut":
        d = src_dict.copy()
        lang = d.pop("lang")

        entity_types = cast(List[str], d.pop("entity_types"))

        language_entities_out = LanguageEntitiesOut(
            lang=lang,
            entity_types=entity_types,
        )

        language_entities_out.additional_properties = d
        return language_entities_out

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
