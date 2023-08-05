from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class SearchResultPipelineLogsBordhunks:
    """  """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SearchResultPipelineLogsBordhunks":
        d = src_dict.copy()
        search_result_pipeline_logs_bordhunks = SearchResultPipelineLogsBordhunks()

        search_result_pipeline_logs_bordhunks.additional_properties = d
        return search_result_pipeline_logs_bordhunks

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
