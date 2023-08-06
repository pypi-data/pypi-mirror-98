import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.analyzer_language import AnalyzerLanguage
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchConfigurationOut")


@attr.s(auto_attribs=True)
class SearchConfigurationOut:
    """ Search Configuration schema for get return. """

    org_id: int
    auto_semantic: bool
    lemma_language: AnalyzerLanguage
    stop_words_language: AnalyzerLanguage
    skip_neural: bool
    metadata_boost: bool
    auto_suggest: bool
    lemmatization: bool
    stop_words: bool
    nb_synonyms: int
    manual_weight: Union[Unset, float] = UNSET
    updated_on: Union[Unset, datetime.datetime] = UNSET
    updated_by: Union[Unset, int] = UNSET
    synonyms_updated_on: Union[Unset, datetime.datetime] = UNSET
    synonyms_updated_by: Union[Unset, int] = UNSET
    synonyms_file: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        org_id = self.org_id
        auto_semantic = self.auto_semantic
        lemma_language = self.lemma_language.value

        stop_words_language = self.stop_words_language.value

        skip_neural = self.skip_neural
        metadata_boost = self.metadata_boost
        auto_suggest = self.auto_suggest
        lemmatization = self.lemmatization
        stop_words = self.stop_words
        nb_synonyms = self.nb_synonyms
        manual_weight = self.manual_weight
        updated_on: Union[Unset, str] = UNSET
        if not isinstance(self.updated_on, Unset):
            updated_on = self.updated_on.isoformat()

        updated_by = self.updated_by
        synonyms_updated_on: Union[Unset, str] = UNSET
        if not isinstance(self.synonyms_updated_on, Unset):
            synonyms_updated_on = self.synonyms_updated_on.isoformat()

        synonyms_updated_by = self.synonyms_updated_by
        synonyms_file = self.synonyms_file

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_id": org_id,
                "auto_semantic": auto_semantic,
                "lemma_language": lemma_language,
                "stop_words_language": stop_words_language,
                "skip_neural": skip_neural,
                "metadata_boost": metadata_boost,
                "auto_suggest": auto_suggest,
                "lemmatization": lemmatization,
                "stop_words": stop_words,
                "nb_synonyms": nb_synonyms,
            }
        )
        if manual_weight is not UNSET:
            field_dict["manual_weight"] = manual_weight
        if updated_on is not UNSET:
            field_dict["updated_on"] = updated_on
        if updated_by is not UNSET:
            field_dict["updated_by"] = updated_by
        if synonyms_updated_on is not UNSET:
            field_dict["synonyms_updated_on"] = synonyms_updated_on
        if synonyms_updated_by is not UNSET:
            field_dict["synonyms_updated_by"] = synonyms_updated_by
        if synonyms_file is not UNSET:
            field_dict["synonyms_file"] = synonyms_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        org_id = d.pop("org_id")

        auto_semantic = d.pop("auto_semantic")

        lemma_language = AnalyzerLanguage(d.pop("lemma_language"))

        stop_words_language = AnalyzerLanguage(d.pop("stop_words_language"))

        skip_neural = d.pop("skip_neural")

        metadata_boost = d.pop("metadata_boost")

        auto_suggest = d.pop("auto_suggest")

        lemmatization = d.pop("lemmatization")

        stop_words = d.pop("stop_words")

        nb_synonyms = d.pop("nb_synonyms")

        manual_weight = d.pop("manual_weight", UNSET)

        updated_on: Union[Unset, datetime.datetime] = UNSET
        _updated_on = d.pop("updated_on", UNSET)
        if not isinstance(_updated_on, Unset):
            updated_on = isoparse(_updated_on)

        updated_by = d.pop("updated_by", UNSET)

        synonyms_updated_on: Union[Unset, datetime.datetime] = UNSET
        _synonyms_updated_on = d.pop("synonyms_updated_on", UNSET)
        if not isinstance(_synonyms_updated_on, Unset):
            synonyms_updated_on = isoparse(_synonyms_updated_on)

        synonyms_updated_by = d.pop("synonyms_updated_by", UNSET)

        synonyms_file = d.pop("synonyms_file", UNSET)

        search_configuration_out = cls(
            org_id=org_id,
            auto_semantic=auto_semantic,
            lemma_language=lemma_language,
            stop_words_language=stop_words_language,
            skip_neural=skip_neural,
            metadata_boost=metadata_boost,
            auto_suggest=auto_suggest,
            lemmatization=lemmatization,
            stop_words=stop_words,
            nb_synonyms=nb_synonyms,
            manual_weight=manual_weight,
            updated_on=updated_on,
            updated_by=updated_by,
            synonyms_updated_on=synonyms_updated_on,
            synonyms_updated_by=synonyms_updated_by,
            synonyms_file=synonyms_file,
        )

        search_configuration_out.additional_properties = d
        return search_configuration_out

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
