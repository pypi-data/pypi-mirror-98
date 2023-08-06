import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.extract_paragraph_config import ExtractParagraphConfig
from ..models.extract_question_config import ExtractQuestionConfig
from ..models.extract_type import ExtractType
from ..models.extract_value_config import ExtractValueConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractModelOut")


@attr.s(auto_attribs=True)
class ExtractModelOut:
    """ Extract model schema to be received on the GET /extract/models response. """

    name: str
    type: ExtractType
    config: Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
    org_id: int
    id: int
    created_on: datetime.datetime
    questionnaire_model_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type = self.type.value

        if isinstance(self.config, ExtractValueConfig):
            config = self.config.to_dict()

        elif isinstance(self.config, ExtractParagraphConfig):
            config = self.config.to_dict()

        else:
            config = self.config.to_dict()

        org_id = self.org_id
        id = self.id
        created_on = self.created_on.isoformat()

        questionnaire_model_id = self.questionnaire_model_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type,
                "config": config,
                "org_id": org_id,
                "id": id,
                "created_on": created_on,
            }
        )
        if questionnaire_model_id is not UNSET:
            field_dict["questionnaire_model_id"] = questionnaire_model_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type = ExtractType(d.pop("type"))

        def _parse_config(data: Any) -> Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]:
            data = None if isinstance(data, Unset) else data
            config: Union[ExtractValueConfig, ExtractParagraphConfig, ExtractQuestionConfig]
            try:
                config = ExtractValueConfig.from_dict(data)

                return config
            except:  # noqa: E722
                pass
            try:
                config = ExtractParagraphConfig.from_dict(data)

                return config
            except:  # noqa: E722
                pass
            config = ExtractQuestionConfig.from_dict(data)

            return config

        config = _parse_config(d.pop("config"))

        org_id = d.pop("org_id")

        id = d.pop("id")

        created_on = isoparse(d.pop("created_on"))

        questionnaire_model_id = d.pop("questionnaire_model_id", UNSET)

        extract_model_out = cls(
            name=name,
            type=type,
            config=config,
            org_id=org_id,
            id=id,
            created_on=created_on,
            questionnaire_model_id=questionnaire_model_id,
        )

        extract_model_out.additional_properties = d
        return extract_model_out

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
