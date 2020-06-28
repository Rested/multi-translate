import logging
from typing import Optional
from urllib.parse import urljoin

import httpx

from engines import BaseTranslationEngine
from errors import (
    DetectionError,
    EngineApiError,
    TranslationEngineNotConfiguredError,
    TranslationError,
)
from models.response import TranslationResponse
from settings import Settings


class YandexEngine(BaseTranslationEngine):
    NAME = "yandex"
    VERSION = "2"

    supports_detection = True

    def __init__(self):
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        self.endpoint = settings.yandex_endpoint
        self.token = settings.yandex_iam_token
        self.folder_id = settings.yandex_folder_id
        if settings.google_svc_account_json_path is None:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: no iam token configured"
            )
        super().__init__()

    def handle_api_error(self, response: httpx.Response):
        if response.status_code >= 500:
            raise EngineApiError(
                f"{self.name_ver} engine returned a status code {response.status_code} response"
            )
        if response.status_code >= 400:
            self._logger.debug("%s got response: %s", self.name_ver, response.text)
            response_json = response.json()
            raise EngineApiError(
                f"{self.name_ver} engine returned error code: {response_json['code']}, message: {response_json['message']}"
            )

    def get_supported_translations(self):
        response = httpx.post(
            urljoin(str(self.endpoint), "languages"),
            headers={"Authorization": f"Bearer {self.token}"},
            json={"folderId": self.folder_id} if self.folder_id else {},
        )
        self.handle_api_error(response)
        response_json = response.json()

        all_languages = [language["code"] for language in response_json["languages"]]
        return {lang: all_languages for lang in all_languages}

    async def translate(
        self,
        source_text: str,
        from_language: Optional[str],
        to_language: str,
        with_alignment: Optional[bool] = False,
    ) -> TranslationResponse:
        await super().translate(
            source_text=source_text,
            to_language=to_language,
            from_language=from_language,
            with_alignment=with_alignment,
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(str(self.endpoint), "translate"),
                json={
                    "texts": [source_text],
                    "targetLanguageCode": to_language,
                    **({"folderId": self.folder_id} if self.folder_id else {}),
                    **({"sourceLanguageCode": from_language} if from_language else {}),
                },
                headers={"Authorization": f"Bearer {self.token}"},
            )
        self.handle_api_error(response)
        response_json = response.json()
        self._logger.debug("%s got response: %s", self.name_ver, response_json)

        detected_language = None
        if from_language is None:
            try:
                detected_language = response_json["translations"][0][
                    "detectedLanguageCode"
                ]
            except (KeyError, IndexError) as e:
                raise DetectionError(
                    f"{self.name_ver} engine could not detect which language the source text is in"
                ) from e

        try:
            translated_text = response_json["translations"][0]["text"]
        except (AttributeError, IndexError) as e:
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
