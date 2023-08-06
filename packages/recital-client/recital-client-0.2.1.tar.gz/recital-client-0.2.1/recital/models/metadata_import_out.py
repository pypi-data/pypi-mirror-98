import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.task_status import TaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataImportOut")


@attr.s(auto_attribs=True)
class MetadataImportOut:
    """ Schema representing the output from metadata import GET. """

    id: int
    org_id: int
    status: TaskStatus
    check_task_id: int
    temp_file_uuid: str
    report_id: int
    started_on: Union[Unset, datetime.datetime] = UNSET
    update_task_id: Union[Unset, int] = UNSET
    n_found_docs: Union[Unset, int] = UNSET
    n_notfound_docs: Union[Unset, int] = UNSET
    n_created_metadata: Union[Unset, int] = UNSET
    n_replaced_metadata: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        org_id = self.org_id
        status = self.status.value

        check_task_id = self.check_task_id
        temp_file_uuid = self.temp_file_uuid
        report_id = self.report_id
        started_on: Union[Unset, str] = UNSET
        if not isinstance(self.started_on, Unset):
            started_on = self.started_on.isoformat()

        update_task_id = self.update_task_id
        n_found_docs = self.n_found_docs
        n_notfound_docs = self.n_notfound_docs
        n_created_metadata = self.n_created_metadata
        n_replaced_metadata = self.n_replaced_metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "status": status,
                "check_task_id": check_task_id,
                "temp_file_uuid": temp_file_uuid,
                "report_id": report_id,
            }
        )
        if started_on is not UNSET:
            field_dict["started_on"] = started_on
        if update_task_id is not UNSET:
            field_dict["update_task_id"] = update_task_id
        if n_found_docs is not UNSET:
            field_dict["n_found_docs"] = n_found_docs
        if n_notfound_docs is not UNSET:
            field_dict["n_notfound_docs"] = n_notfound_docs
        if n_created_metadata is not UNSET:
            field_dict["n_created_metadata"] = n_created_metadata
        if n_replaced_metadata is not UNSET:
            field_dict["n_replaced_metadata"] = n_replaced_metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        org_id = d.pop("org_id")

        status = TaskStatus(d.pop("status"))

        check_task_id = d.pop("check_task_id")

        temp_file_uuid = d.pop("temp_file_uuid")

        report_id = d.pop("report_id")

        started_on: Union[Unset, datetime.datetime] = UNSET
        _started_on = d.pop("started_on", UNSET)
        if not isinstance(_started_on, Unset):
            started_on = isoparse(_started_on)

        update_task_id = d.pop("update_task_id", UNSET)

        n_found_docs = d.pop("n_found_docs", UNSET)

        n_notfound_docs = d.pop("n_notfound_docs", UNSET)

        n_created_metadata = d.pop("n_created_metadata", UNSET)

        n_replaced_metadata = d.pop("n_replaced_metadata", UNSET)

        metadata_import_out = cls(
            id=id,
            org_id=org_id,
            status=status,
            check_task_id=check_task_id,
            temp_file_uuid=temp_file_uuid,
            report_id=report_id,
            started_on=started_on,
            update_task_id=update_task_id,
            n_found_docs=n_found_docs,
            n_notfound_docs=n_notfound_docs,
            n_created_metadata=n_created_metadata,
            n_replaced_metadata=n_replaced_metadata,
        )

        metadata_import_out.additional_properties = d
        return metadata_import_out

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
