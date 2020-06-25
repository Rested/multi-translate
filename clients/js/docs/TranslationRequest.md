# FastApi.TranslationRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sourceText** | **String** | The text to be translated | 
**toLanguage** | **String** | The ISO-639-1 code of the language to translate the text to | 
**fromLanguage** | **String** | The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted | [optional] 
**preferredEngine** | **String** | Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best | [optional] [default to &#39;best&#39;]
**withAlignment** | **Boolean** | Whether to return word alignment information or not | [optional] [default to false]
**fallback** | **Boolean** | Whether to fallback to the best available engine if the preferred engine does not succeed | [optional] [default to false]


