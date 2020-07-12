/**
 * multi-translate
 * Multi-Translate is a unified interface on top of various translate APIs providing optimal translations, persistence, fallback.
 *
 * The version of the OpenAPI document: 0.6.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';

/**
 * The TranslationResponse model module.
 * @module model/TranslationResponse
 * @version 0.6.0
 */
class TranslationResponse {
    /**
     * Constructs a new <code>TranslationResponse</code>.
     * @alias module:model/TranslationResponse
     * @param engine {String} 
     * @param engineVersion {String} 
     * @param fromLanguage {String} 
     * @param toLanguage {String} 
     * @param sourceText {String} 
     * @param translatedText {String} 
     */
    constructor(engine, engineVersion, fromLanguage, toLanguage, sourceText, translatedText) { 
        
        TranslationResponse.initialize(this, engine, engineVersion, fromLanguage, toLanguage, sourceText, translatedText);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, engine, engineVersion, fromLanguage, toLanguage, sourceText, translatedText) { 
        obj['engine'] = engine;
        obj['engine_version'] = engineVersion;
        obj['from_language'] = fromLanguage;
        obj['to_language'] = toLanguage;
        obj['source_text'] = sourceText;
        obj['translated_text'] = translatedText;
    }

    /**
     * Constructs a <code>TranslationResponse</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/TranslationResponse} obj Optional instance to populate.
     * @return {module:model/TranslationResponse} The populated <code>TranslationResponse</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new TranslationResponse();

            if (data.hasOwnProperty('engine')) {
                obj['engine'] = ApiClient.convertToType(data['engine'], 'String');
            }
            if (data.hasOwnProperty('engine_version')) {
                obj['engine_version'] = ApiClient.convertToType(data['engine_version'], 'String');
            }
            if (data.hasOwnProperty('detected_language_confidence')) {
                obj['detected_language_confidence'] = ApiClient.convertToType(data['detected_language_confidence'], 'Number');
            }
            if (data.hasOwnProperty('from_language')) {
                obj['from_language'] = ApiClient.convertToType(data['from_language'], 'String');
            }
            if (data.hasOwnProperty('to_language')) {
                obj['to_language'] = ApiClient.convertToType(data['to_language'], 'String');
            }
            if (data.hasOwnProperty('source_text')) {
                obj['source_text'] = ApiClient.convertToType(data['source_text'], 'String');
            }
            if (data.hasOwnProperty('translated_text')) {
                obj['translated_text'] = ApiClient.convertToType(data['translated_text'], 'String');
            }
            if (data.hasOwnProperty('alignment')) {
                obj['alignment'] = ApiClient.convertToType(data['alignment'], [{'String': {'String': 'String'}}]);
            }
        }
        return obj;
    }


}

/**
 * @member {String} engine
 */
TranslationResponse.prototype['engine'] = undefined;

/**
 * @member {String} engine_version
 */
TranslationResponse.prototype['engine_version'] = undefined;

/**
 * @member {Number} detected_language_confidence
 */
TranslationResponse.prototype['detected_language_confidence'] = undefined;

/**
 * @member {String} from_language
 */
TranslationResponse.prototype['from_language'] = undefined;

/**
 * @member {String} to_language
 */
TranslationResponse.prototype['to_language'] = undefined;

/**
 * @member {String} source_text
 */
TranslationResponse.prototype['source_text'] = undefined;

/**
 * @member {String} translated_text
 */
TranslationResponse.prototype['translated_text'] = undefined;

/**
 * @member {Array.<Object.<String, Object.<String, String>>>} alignment
 */
TranslationResponse.prototype['alignment'] = undefined;






export default TranslationResponse;

