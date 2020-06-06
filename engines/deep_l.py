import logging
from typing import Optional
from urllib.parse import urljoin

import httpx

from engines import BaseTranslationEngine
from errors import TranslationEngineNotConfiguredError, EngineApiError, DetectionError, TranslationError
from models import TranslationResponse
from settings import Settings


def convert_upper_language_country_combo(lang_country_combo: str) -> str:
    split_code = lang_country_combo.split("-")
    if len(split_code) == 1:
        return split_code[0].casefold()
    return f"{split_code[0].casefold()}-{split_code[1]}"


class DeepLEngine(BaseTranslationEngine):
    NAME = "deepl"
    VERSION = "2"

    supports_detection = True

    def __init__(self):
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        self.endpoint = settings.deep_l_endpoint
        self.auth_key = settings.deep_l_auth_key
        if self.auth_key is None:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: no auth key configured"
            )

        super().__init__()

    def handle_api_error(self, response: httpx.Response):
        # todo: use this approach of using response instead of response json for other engines
        if response.status_code >= 500:
            raise EngineApiError(f"{self.name_ver} engine returned a status code {response.status_code} response")
        if response.status_code >= 400:
            self._logger.debug("%s got response: %s", self.name_ver, response.text)
            response_json = response.json()
            raise EngineApiError(
                f"{self.name_ver} engine returned error message: {response_json['message']}"
            )

    def get_supported_translations(self):
        languages_supported_url = urljoin(str(self.endpoint), "languages")
        self._logger.debug("sending request to %s", languages_supported_url)
        response = httpx.get(languages_supported_url, params={
            "auth_key": self.auth_key
        }, headers={
            "User-Agent": "MultiTranslate",
            "Accept": "*/*"
        })
        self.handle_api_error(response)
        response_json = response.json()

        all_languages = [convert_upper_language_country_combo(language['language']) for language in response_json]
        return {lang: all_languages for lang in all_languages}

    async def translate(
            self,
            source_text: str,
            from_language: Optional[str],
            to_language: str,
            with_alignment: Optional[bool] = False,
    ) -> TranslationResponse:
        await super().translate(source_text=source_text, to_language=to_language, from_language=from_language,
                                with_alignment=with_alignment)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(str(self.endpoint), "translate"),
                data={
                    "text": source_text, "target_lang": to_language,
                    "auth_key": self.auth_key,
                    **({"source_lang": from_language} if from_language else {})
                },
                headers={
                    "User-Agent": "MultiTranslate"
                }
            )
        self.handle_api_error(response)
        response_json = response.json()
        self._logger.debug("%s got response: %s", self.name_ver, response_json)

        detected_language = None
        if from_language is None:
            try:
                detected_language = convert_upper_language_country_combo(
                    lang_country_combo=response_json["translations"][0]["detected_source_language"])
            except (KeyError, IndexError) as e:
                raise DetectionError(
                    f"{self.name_ver} engine could not detect which language the source text is in"
                ) from e

        try:
            translated_text = response_json["translations"][0]["text"]
        except AttributeError as e:
            raise TranslationError(
                f"{self.name_ver} engine could not translate the given text"
            ) from e

        return TranslationResponse(
            engine=self.NAME,
            engine_version=self.VERSION,
            source_text=source_text,
            from_language=from_language or detected_language,
            to_language=to_language,
            detected_language_confidence=None,
            translated_text=translated_text,
            alignment=None,
        )
