from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.indexing_error_in_args import IndexingErrorInArgs
from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexingErrorIn")


@attr.s(auto_attribs=True)
class IndexingErrorIn:
    """ Indexing error in schema. """

    file_path: str
    code: int
    message: str
    args: IndexingErrorInArgs
    proc_docs: Union[Unset, int] = 1
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_path = self.file_path
        code = self.code
        message = self.message
        args = self.args.to_dict()

        proc_docs = self.proc_docs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_path": file_path,
                "code": code,
                "message": message,
                "args": args,
            }
        )
        if proc_docs is not UNSET:
            field_dict["proc_docs"] = proc_docs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_path = d.pop("file_path")

        code = d.pop("code")

        message = d.pop("message")

        args = IndexingErrorInArgs.from_dict(d.pop("args"))

        proc_docs = d.pop("proc_docs", UNSET)

        indexing_error_in = cls(
            file_path=file_path,
            code=code,
            message=message,
            args=args,
            proc_docs=proc_docs,
        )

        indexing_error_in.additional_properties = d
        return indexing_error_in

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
