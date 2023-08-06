from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="IndexingTaskUpdate")


@attr.s(auto_attribs=True)
class IndexingTaskUpdate:
    """ Indexing task schema. """

    proc_docs: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        proc_docs = self.proc_docs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "proc_docs": proc_docs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        proc_docs = d.pop("proc_docs")

        indexing_task_update = cls(
            proc_docs=proc_docs,
        )

        indexing_task_update.additional_properties = d
        return indexing_task_update

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
