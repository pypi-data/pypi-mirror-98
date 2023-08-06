from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.indexing_error_in_db_args import IndexingErrorInDBArgs

T = TypeVar("T", bound="IndexingErrorInDB")


@attr.s(auto_attribs=True)
class IndexingErrorInDB:
    """ Indexing error schema for database input. """

    file_path: str
    code: int
    message: str
    args: IndexingErrorInDBArgs
    task_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_path = self.file_path
        code = self.code
        message = self.message
        args = self.args.to_dict()

        task_id = self.task_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_path": file_path,
                "code": code,
                "message": message,
                "args": args,
                "task_id": task_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_path = d.pop("file_path")

        code = d.pop("code")

        message = d.pop("message")

        args = IndexingErrorInDBArgs.from_dict(d.pop("args"))

        task_id = d.pop("task_id")

        indexing_error_in_db = cls(
            file_path=file_path,
            code=code,
            message=message,
            args=args,
            task_id=task_id,
        )

        indexing_error_in_db.additional_properties = d
        return indexing_error_in_db

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
