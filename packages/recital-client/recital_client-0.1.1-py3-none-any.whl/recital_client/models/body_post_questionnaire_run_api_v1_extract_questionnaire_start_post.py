from io import BytesIO
from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, File, Unset


@attr.s(auto_attribs=True)
class BodyPostQuestionnaireRunApiV1ExtractQuestionnaireStart_Post:
    """  """

    excel_questions: Union[Unset, File] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        excel_questions: Union[Unset, File] = UNSET
        if not isinstance(self.excel_questions, Unset):
            excel_questions = self.excel_questions.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if excel_questions is not UNSET:
            field_dict["excel_questions"] = excel_questions

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BodyPostQuestionnaireRunApiV1ExtractQuestionnaireStart_Post":
        d = src_dict.copy()
        excel_questions = File(payload=BytesIO(d.pop("excel_questions", UNSET)))

        body_post_questionnaire_run_api_v1_extract_questionnaire_start_post = (
            BodyPostQuestionnaireRunApiV1ExtractQuestionnaireStart_Post(
                excel_questions=excel_questions,
            )
        )

        body_post_questionnaire_run_api_v1_extract_questionnaire_start_post.additional_properties = d
        return body_post_questionnaire_run_api_v1_extract_questionnaire_start_post

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
