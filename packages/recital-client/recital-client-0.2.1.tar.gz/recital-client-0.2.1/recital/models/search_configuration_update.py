from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.analyzer_language import AnalyzerLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchConfigurationUpdate")


@attr.s(auto_attribs=True)
class SearchConfigurationUpdate:
    """ Search Configuration update schema. """

    auto_semantic: Union[Unset, bool] = UNSET
    manual_weight: Union[Unset, float] = UNSET
    lemma_language: Union[Unset, AnalyzerLanguage] = UNSET
    stop_words_language: Union[Unset, AnalyzerLanguage] = UNSET
    skip_neural: Union[Unset, bool] = UNSET
    metadata_boost: Union[Unset, bool] = UNSET
    auto_suggest: Union[Unset, bool] = UNSET
    lemmatization: Union[Unset, bool] = UNSET
    stop_words: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auto_semantic = self.auto_semantic
        manual_weight = self.manual_weight
        lemma_language: Union[Unset, AnalyzerLanguage] = UNSET
        if not isinstance(self.lemma_language, Unset):
            lemma_language = self.lemma_language

        stop_words_language: Union[Unset, AnalyzerLanguage] = UNSET
        if not isinstance(self.stop_words_language, Unset):
            stop_words_language = self.stop_words_language

        skip_neural = self.skip_neural
        metadata_boost = self.metadata_boost
        auto_suggest = self.auto_suggest
        lemmatization = self.lemmatization
        stop_words = self.stop_words

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_semantic is not UNSET:
            field_dict["auto_semantic"] = auto_semantic
        if manual_weight is not UNSET:
            field_dict["manual_weight"] = manual_weight
        if lemma_language is not UNSET:
            field_dict["lemma_language"] = lemma_language
        if stop_words_language is not UNSET:
            field_dict["stop_words_language"] = stop_words_language
        if skip_neural is not UNSET:
            field_dict["skip_neural"] = skip_neural
        if metadata_boost is not UNSET:
            field_dict["metadata_boost"] = metadata_boost
        if auto_suggest is not UNSET:
            field_dict["auto_suggest"] = auto_suggest
        if lemmatization is not UNSET:
            field_dict["lemmatization"] = lemmatization
        if stop_words is not UNSET:
            field_dict["stop_words"] = stop_words

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        auto_semantic = d.pop("auto_semantic", UNSET)

        manual_weight = d.pop("manual_weight", UNSET)

        lemma_language: Union[Unset, AnalyzerLanguage] = UNSET
        _lemma_language = d.pop("lemma_language", UNSET)
        if not isinstance(_lemma_language, Unset):
            lemma_language = AnalyzerLanguage(_lemma_language)

        stop_words_language: Union[Unset, AnalyzerLanguage] = UNSET
        _stop_words_language = d.pop("stop_words_language", UNSET)
        if not isinstance(_stop_words_language, Unset):
            stop_words_language = AnalyzerLanguage(_stop_words_language)

        skip_neural = d.pop("skip_neural", UNSET)

        metadata_boost = d.pop("metadata_boost", UNSET)

        auto_suggest = d.pop("auto_suggest", UNSET)

        lemmatization = d.pop("lemmatization", UNSET)

        stop_words = d.pop("stop_words", UNSET)

        search_configuration_update = cls(
            auto_semantic=auto_semantic,
            manual_weight=manual_weight,
            lemma_language=lemma_language,
            stop_words_language=stop_words_language,
            skip_neural=skip_neural,
            metadata_boost=metadata_boost,
            auto_suggest=auto_suggest,
            lemmatization=lemmatization,
            stop_words=stop_words,
        )

        search_configuration_update.additional_properties = d
        return search_configuration_update

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
