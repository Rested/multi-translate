/**
 * multi-translate
 * Multi-Translate is a unified interface on top of various translate APIs providing optimal translations, persistence, fallback.
 *
 * The version of the OpenAPI document: 0.5.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */


import ApiClient from './ApiClient';
import HTTPValidationError from './model/HTTPValidationError';
import TranslationRequest from './model/TranslationRequest';
import TranslationResponse from './model/TranslationResponse';
import ValidationError from './model/ValidationError';
import DefaultApi from './api/DefaultApi';


/**
* Multi_Translate_is_a_unified_interface_on_top_of_various_translate_APIs_providing_optimal_translations_persistence_fallback_.<br>
* The <code>index</code> module provides access to constructors for all the classes which comprise the public API.
* <p>
* An AMD (recommended!) or CommonJS application will generally do something equivalent to the following:
* <pre>
* var @RekonOssMultiTranslate = require('index'); // See note below*.
* var xxxSvc = new @RekonOssMultiTranslate.XxxApi(); // Allocate the API class we're going to use.
* var yyyModel = new @RekonOssMultiTranslate.Yyy(); // Construct a model instance.
* yyyModel.someProperty = 'someValue';
* ...
* var zzz = xxxSvc.doSomething(yyyModel); // Invoke the service.
* ...
* </pre>
* <em>*NOTE: For a top-level AMD script, use require(['index'], function(){...})
* and put the application logic within the callback function.</em>
* </p>
* <p>
* A non-AMD browser application (discouraged) might do something like this:
* <pre>
* var xxxSvc = new @RekonOssMultiTranslate.XxxApi(); // Allocate the API class we're going to use.
* var yyy = new @RekonOssMultiTranslate.Yyy(); // Construct a model instance.
* yyyModel.someProperty = 'someValue';
* ...
* var zzz = xxxSvc.doSomething(yyyModel); // Invoke the service.
* ...
* </pre>
* </p>
* @module index
* @version 0.5.0
*/
export {
    /**
     * The ApiClient constructor.
     * @property {module:ApiClient}
     */
    ApiClient,

    /**
     * The HTTPValidationError model constructor.
     * @property {module:model/HTTPValidationError}
     */
    HTTPValidationError,

    /**
     * The TranslationRequest model constructor.
     * @property {module:model/TranslationRequest}
     */
    TranslationRequest,

    /**
     * The TranslationResponse model constructor.
     * @property {module:model/TranslationResponse}
     */
    TranslationResponse,

    /**
     * The ValidationError model constructor.
     * @property {module:model/ValidationError}
     */
    ValidationError,

    /**
    * The DefaultApi service constructor.
    * @property {module:api/DefaultApi}
    */
    DefaultApi
};
