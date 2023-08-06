from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ArchivesOut")


@attr.s(auto_attribs=True)
class ArchivesOut:
    """ Archives schema for the POST route. """

    archive_size: int
    uncompress_bkg_task_id: int
    indexing_bkg_task_id: int
    indexing_report_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        archive_size = self.archive_size
        uncompress_bkg_task_id = self.uncompress_bkg_task_id
        indexing_bkg_task_id = self.indexing_bkg_task_id
        indexing_report_id = self.indexing_report_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "archive_size": archive_size,
                "uncompress_bkg_task_id": uncompress_bkg_task_id,
                "indexing_bkg_task_id": indexing_bkg_task_id,
                "indexing_report_id": indexing_report_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        archive_size = d.pop("archive_size")

        uncompress_bkg_task_id = d.pop("uncompress_bkg_task_id")

        indexing_bkg_task_id = d.pop("indexing_bkg_task_id")

        indexing_report_id = d.pop("indexing_report_id")

        archives_out = cls(
            archive_size=archive_size,
            uncompress_bkg_task_id=uncompress_bkg_task_id,
            indexing_bkg_task_id=indexing_bkg_task_id,
            indexing_report_id=indexing_report_id,
        )

        archives_out.additional_properties = d
        return archives_out

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
