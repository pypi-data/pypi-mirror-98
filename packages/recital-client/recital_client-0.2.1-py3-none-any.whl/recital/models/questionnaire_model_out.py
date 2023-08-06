from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="QuestionnaireModelOut")


@attr.s(auto_attribs=True)
class QuestionnaireModelOut:
    """ Questionnaire model schema for GET methods. """

    name: str
    org_id: int
    id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        org_id = self.org_id
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "org_id": org_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        org_id = d.pop("org_id")

        id = d.pop("id")

        questionnaire_model_out = cls(
            name=name,
            org_id=org_id,
            id=id,
        )

        questionnaire_model_out.additional_properties = d
        return questionnaire_model_out

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
