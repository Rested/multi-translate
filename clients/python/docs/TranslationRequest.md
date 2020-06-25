# TranslationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_text** | **str** | The text to be translated | 
**to_language** | **str** | The ISO-639-1 code of the language to translate the text to | 
**from_language** | **str** | The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted | [optional] 
**preferred_engine** | **str** | Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best | [optional] [default to 'best']
**with_alignment** | **bool** | Whether to return word alignment information or not | [optional] [default to False]
**fallback** | **bool** | Whether to fallback to the best available engine if the preferred engine does not succeed | [optional] [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


