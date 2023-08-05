from typing import Any, Dict, List, Union, cast

import attr

from ..models.search_result_pipeline_logs_bordhunks import SearchResultPipelineLogsBordhunks
from ..models.search_result_pipeline_logs_documents import SearchResultPipelineLogsDocuments
from ..models.search_result_pipeline_logs_lexicahunks import SearchResultPipelineLogsLexicahunks
from ..models.search_result_pipeline_logs_semantihunks import SearchResultPipelineLogsSemantihunks
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class SearchResultPipelineLogs:
    """ Schema for search pipeline logs """

    documents: Union[SearchResultPipelineLogsDocuments, Unset] = UNSET
    lexical_chunks: Union[SearchResultPipelineLogsLexicahunks, Unset] = UNSET
    semantic_chunks: Union[SearchResultPipelineLogsSemantihunks, Unset] = UNSET
    borda_chunks: Union[SearchResultPipelineLogsBordhunks, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        documents: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.documents, Unset):
            documents = self.documents.to_dict()

        lexical_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lexical_chunks, Unset):
            lexical_chunks = self.lexical_chunks.to_dict()

        semantic_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_chunks, Unset):
            semantic_chunks = self.semantic_chunks.to_dict()

        borda_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.borda_chunks, Unset):
            borda_chunks = self.borda_chunks.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if documents is not UNSET:
            field_dict["documents"] = documents
        if lexical_chunks is not UNSET:
            field_dict["lexical_chunks"] = lexical_chunks
        if semantic_chunks is not UNSET:
            field_dict["semantic_chunks"] = semantic_chunks
        if borda_chunks is not UNSET:
            field_dict["borda_chunks"] = borda_chunks

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "SearchResultPipelineLogs":
        d = src_dict.copy()
        documents: Union[SearchResultPipelineLogsDocuments, Unset] = UNSET
        _documents = d.pop("documents", UNSET)
        if _documents is not None and not isinstance(_documents, Unset):
            documents = SearchResultPipelineLogsDocuments.from_dict(cast(Dict[str, Any], _documents))

        lexical_chunks: Union[SearchResultPipelineLogsLexicahunks, Unset] = UNSET
        _lexical_chunks = d.pop("lexical_chunks", UNSET)
        if _lexical_chunks is not None and not isinstance(_lexical_chunks, Unset):
            lexical_chunks = SearchResultPipelineLogsLexicahunks.from_dict(cast(Dict[str, Any], _lexical_chunks))

        semantic_chunks: Union[SearchResultPipelineLogsSemantihunks, Unset] = UNSET
        _semantic_chunks = d.pop("semantic_chunks", UNSET)
        if _semantic_chunks is not None and not isinstance(_semantic_chunks, Unset):
            semantic_chunks = SearchResultPipelineLogsSemantihunks.from_dict(cast(Dict[str, Any], _semantic_chunks))

        borda_chunks: Union[SearchResultPipelineLogsBordhunks, Unset] = UNSET
        _borda_chunks = d.pop("borda_chunks", UNSET)
        if _borda_chunks is not None and not isinstance(_borda_chunks, Unset):
            borda_chunks = SearchResultPipelineLogsBordhunks.from_dict(cast(Dict[str, Any], _borda_chunks))

        search_result_pipeline_logs = SearchResultPipelineLogs(
            documents=documents,
            lexical_chunks=lexical_chunks,
            semantic_chunks=semantic_chunks,
            borda_chunks=borda_chunks,
        )

        search_result_pipeline_logs.additional_properties = d
        return search_result_pipeline_logs

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
