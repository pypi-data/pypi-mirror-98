from io import BytesIO
from typing import Any, Dict, List

import attr

from ..types import File


@attr.s(auto_attribs=True)
class GetVersionStyledHtmlPagesResponseersiotyletmagepileersionersiotyletmet:
    """  """

    additional_properties: Dict[str, File] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_tuple()

        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "GetVersionStyledHtmlPagesResponseersiotyletmagepileersionersiotyletmet":
        d = src_dict.copy()
        get_version_styled_html_pages_responseersiotyletmagepileersionersiotyletmet = (
            GetVersionStyledHtmlPagesResponseersiotyletmagepileersionersiotyletmet()
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = File(payload=BytesIO(prop_dict))

            additional_properties[prop_name] = additional_property

        get_version_styled_html_pages_responseersiotyletmagepileersionersiotyletmet.additional_properties = (
            additional_properties
        )
        return get_version_styled_html_pages_responseersiotyletmagepileersionersiotyletmet

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> File:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: File) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
