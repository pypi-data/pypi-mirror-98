from typing import Any, Dict, List, Union, cast

import attr

from ..models.questionnaire import Questionnaire
from ..models.questionnaire_model_create import QuestionnaireModelCreate
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class QuestionnaireCreate:
    """ Questionnaire schema to be sent on POST /questionnaire endpoint. """

    questionnaire: Questionnaire
    model: Union[QuestionnaireModelCreate, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        questionnaire = self.questionnaire.to_dict()

        model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "questionnaire": questionnaire,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "QuestionnaireCreate":
        d = src_dict.copy()
        questionnaire = Questionnaire.from_dict(d.pop("questionnaire"))

        model: Union[QuestionnaireModelCreate, Unset] = UNSET
        _model = d.pop("model", UNSET)
        if _model is not None and not isinstance(_model, Unset):
            model = QuestionnaireModelCreate.from_dict(cast(Dict[str, Any], _model))

        questionnaire_create = QuestionnaireCreate(
            questionnaire=questionnaire,
            model=model,
        )

        questionnaire_create.additional_properties = d
        return questionnaire_create

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
