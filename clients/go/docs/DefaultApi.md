# \DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**GetSupportedEnginesAvailableEnginesGet**](DefaultApi.md#GetSupportedEnginesAvailableEnginesGet) | **Get** /available-engines | Get Supported Engines
[**GetSupportedLanguagesSupportedLanguagesGet**](DefaultApi.md#GetSupportedLanguagesSupportedLanguagesGet) | **Get** /supported-languages | Get Supported Languages
[**ReadyGet**](DefaultApi.md#ReadyGet) | **Get** / | Ready
[**TranslatePostTranslatePost**](DefaultApi.md#TranslatePostTranslatePost) | **Post** /translate | Translate Post
[**TranslateTranslateGet**](DefaultApi.md#TranslateTranslateGet) | **Get** /translate | Translate



## GetSupportedEnginesAvailableEnginesGet

> []string GetSupportedEnginesAvailableEnginesGet(ctx, )

Get Supported Engines

### Required Parameters

This endpoint does not need any parameter.

### Return type

**[]string**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## GetSupportedLanguagesSupportedLanguagesGet

> map[string][]string GetSupportedLanguagesSupportedLanguagesGet(ctx, )

Get Supported Languages

### Required Parameters

This endpoint does not need any parameter.

### Return type

[**map[string][]string**](array.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## ReadyGet

> string ReadyGet(ctx, )

Ready

### Required Parameters

This endpoint does not need any parameter.

### Return type

**string**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## TranslatePostTranslatePost

> TranslationResponse TranslatePostTranslatePost(ctx, translationRequest)

Translate Post

### Required Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**translationRequest** | [**TranslationRequest**](TranslationRequest.md)|  | 

### Return type

[**TranslationResponse**](TranslationResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)


## TranslateTranslateGet

> TranslationResponse TranslateTranslateGet(ctx, sourceText, toLanguage, optional)

Translate

### Required Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
**ctx** | **context.Context** | context for authentication, logging, cancellation, deadlines, tracing, etc.
**sourceText** | **string**| The text to be translated | 
**toLanguage** | **string**| The ISO-639-1 code of the language to translate the text to | 
 **optional** | ***TranslateTranslateGetOpts** | optional parameters | nil if no parameters

### Optional Parameters

Optional parameters are passed through a pointer to a TranslateTranslateGetOpts struct


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------


 **fromLanguage** | **optional.String**| The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted | 
 **preferredEngine** | **optional.String**| Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best | [default to best]
 **withAlignment** | **optional.Bool**| Whether to return word alignment information or not | [default to false]
 **fallback** | **optional.Bool**| Whether to fallback to the best available engine if the preferred engine does not succeed | [default to false]

### Return type

[**TranslationResponse**](TranslationResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints)
[[Back to Model list]](../README.md#documentation-for-models)
[[Back to README]](../README.md)

