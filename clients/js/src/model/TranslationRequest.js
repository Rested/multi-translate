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

import ApiClient from '../ApiClient';

/**
 * The TranslationRequest model module.
 * @module model/TranslationRequest
 * @version 0.5.0
 */
class TranslationRequest {
    /**
     * Constructs a new <code>TranslationRequest</code>.
     * @alias module:model/TranslationRequest
     * @param sourceText {String} The text to be translated
     * @param toLanguage {String} The ISO-639-1 code of the language to translate the text to
     */
    constructor(sourceText, toLanguage) { 
        
        TranslationRequest.initialize(this, sourceText, toLanguage);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, sourceText, toLanguage) { 
        obj['source_text'] = sourceText;
        obj['to_language'] = toLanguage;
    }

    /**
     * Constructs a <code>TranslationRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/TranslationRequest} obj Optional instance to populate.
     * @return {module:model/TranslationRequest} The populated <code>TranslationRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new TranslationRequest();

            if (data.hasOwnProperty('source_text')) {
                obj['source_text'] = ApiClient.convertToType(data['source_text'], 'String');
            }
            if (data.hasOwnProperty('to_language')) {
                obj['to_language'] = ApiClient.convertToType(data['to_language'], 'String');
            }
            if (data.hasOwnProperty('from_language')) {
                obj['from_language'] = ApiClient.convertToType(data['from_language'], 'String');
            }
            if (data.hasOwnProperty('preferred_engine')) {
                obj['preferred_engine'] = ApiClient.convertToType(data['preferred_engine'], 'String');
            }
            if (data.hasOwnProperty('with_alignment')) {
                obj['with_alignment'] = ApiClient.convertToType(data['with_alignment'], 'Boolean');
            }
            if (data.hasOwnProperty('fallback')) {
                obj['fallback'] = ApiClient.convertToType(data['fallback'], 'Boolean');
            }
        }
        return obj;
    }


}

/**
 * The text to be translated
 * @member {String} source_text
 */
TranslationRequest.prototype['source_text'] = undefined;

/**
 * The ISO-639-1 code of the language to translate the text to
 * @member {String} to_language
 */
TranslationRequest.prototype['to_language'] = undefined;

/**
 * The ISO-639-1 code of the language to translate the text from - if notspecified then detection will be attempted
 * @member {String} from_language
 */
TranslationRequest.prototype['from_language'] = undefined;

/**
 * Which translation engine to use. Choices are microsoft, google, amazon, papago, deepl, yandex and best
 * @member {String} preferred_engine
 * @default 'best'
 */
TranslationRequest.prototype['preferred_engine'] = 'best';

/**
 * Whether to return word alignment information or not
 * @member {Boolean} with_alignment
 * @default false
 */
TranslationRequest.prototype['with_alignment'] = false;

/**
 * Whether to fallback to the best available engine if the preferred engine does not succeed
 * @member {Boolean} fallback
 * @default false
 */
TranslationRequest.prototype['fallback'] = false;






export default TranslationRequest;

