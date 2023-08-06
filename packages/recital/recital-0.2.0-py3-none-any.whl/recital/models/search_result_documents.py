from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.document_result import DocumentResult
from ..models.search_result_documents_documents_item import SearchResultDocumentsDocumentsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultDocuments")


@attr.s(auto_attribs=True)
class SearchResultDocuments:
    """ Schema for search result documents. """

    query_id: int
    total_documents: int
    documents: Union[List[DocumentResult], List[SearchResultDocumentsDocumentsItem]]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_id = self.query_id
        total_documents = self.total_documents
        if isinstance(self.documents, list):
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()

                documents.append(documents_item)

        else:
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()

                documents.append(documents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_id": query_id,
                "total_documents": total_documents,
                "documents": documents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query_id = d.pop("query_id")

        total_documents = d.pop("total_documents")

        def _parse_documents(data: Any) -> Union[List[DocumentResult], List[SearchResultDocumentsDocumentsItem]]:
            data = None if isinstance(data, Unset) else data
            documents: Union[List[DocumentResult], List[SearchResultDocumentsDocumentsItem]]
            try:
                documents = UNSET
                _documents = data
                for documents_item_data in _documents:
                    documents_item = DocumentResult.from_dict(documents_item_data)

                    documents.append(documents_item)

                return documents
            except:  # noqa: E722
                pass
            documents = UNSET
            _documents = data
            for documents_item_data in _documents:
                documents_item = SearchResultDocumentsDocumentsItem.from_dict(documents_item_data)

                documents.append(documents_item)

            return documents

        documents = _parse_documents(d.pop("documents"))

        search_result_documents = cls(
            query_id=query_id,
            total_documents=total_documents,
            documents=documents,
        )

        search_result_documents.additional_properties = d
        return search_result_documents

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
