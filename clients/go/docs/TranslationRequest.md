# TranslationRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**SourceText** | **string** | The text to be translated | 
**ToLanguage** | **string** | The ISO-639-1 code of the language to translate the text to | 
**FromLanguage** | **string** | The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted | [optional] 
**PreferredEngine** | **string** | Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best | [optional] [default to best]
**WithAlignment** | **bool** | Whether to return word alignment information or not | [optional] [default to false]
**Fallback** | **bool** | Whether to fallback to the best available engine if the preferred engine does not succeed | [optional] [default to false]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


