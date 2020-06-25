# multitranslateclient.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ready_get**](DefaultApi.md#ready_get) | **GET** / | Ready
[**translate_post_translate_post**](DefaultApi.md#translate_post_translate_post) | **POST** /translate | Translate Post
[**translate_translate_get**](DefaultApi.md#translate_translate_get) | **GET** /translate | Translate


# **ready_get**
> object ready_get()

Ready

### Example

```python
from __future__ import print_function
import time
import multitranslateclient
from multitranslateclient.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multitranslateclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with multitranslateclient.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = multitranslateclient.DefaultApi(api_client)
    
    try:
        # Ready
        api_response = api_instance.ready_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->ready_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **translate_post_translate_post**
> TranslationResponse translate_post_translate_post(translation_request)

Translate Post

### Example

```python
from __future__ import print_function
import time
import multitranslateclient
from multitranslateclient.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multitranslateclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with multitranslateclient.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = multitranslateclient.DefaultApi(api_client)
    translation_request = multitranslateclient.TranslationRequest() # TranslationRequest | 

    try:
        # Translate Post
        api_response = api_instance.translate_post_translate_post(translation_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->translate_post_translate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **translation_request** | [**TranslationRequest**](TranslationRequest.md)|  | 

### Return type

[**TranslationResponse**](TranslationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **translate_translate_get**
> TranslationResponse translate_translate_get(source_text, to_language, from_language=from_language, preferred_engine=preferred_engine, with_alignment=with_alignment, fallback=fallback)

Translate

### Example

```python
from __future__ import print_function
import time
import multitranslateclient
from multitranslateclient.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multitranslateclient.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with multitranslateclient.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = multitranslateclient.DefaultApi(api_client)
    source_text = 'source_text_example' # str | The text to be translated
to_language = 'to_language_example' # str | The ISO-639-1 code of the language to translate the text to
from_language = 'from_language_example' # str | The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted (optional)
preferred_engine = 'best' # str | Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best (optional) (default to 'best')
with_alignment = False # bool | Whether to return word alignment information or not (optional) (default to False)
fallback = False # bool | Whether to fallback to the best available engine if the preferred engine does not succeed (optional) (default to False)

    try:
        # Translate
        api_response = api_instance.translate_translate_get(source_text, to_language, from_language=from_language, preferred_engine=preferred_engine, with_alignment=with_alignment, fallback=fallback)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->translate_translate_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source_text** | **str**| The text to be translated | 
 **to_language** | **str**| The ISO-639-1 code of the language to translate the text to | 
 **from_language** | **str**| The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted | [optional] 
 **preferred_engine** | **str**| Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best | [optional] [default to &#39;best&#39;]
 **with_alignment** | **bool**| Whether to return word alignment information or not | [optional] [default to False]
 **fallback** | **bool**| Whether to fallback to the best available engine if the preferred engine does not succeed | [optional] [default to False]

### Return type

[**TranslationResponse**](TranslationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

