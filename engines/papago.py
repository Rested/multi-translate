import logging
from typing import Dict, Optional

import httpx

from engines.base import BaseTranslationEngine
from errors import EngineApiError, TranslationError, TranslationEngineNotConfiguredError
from models.response import TranslationResponse
from settings import Settings


class PapagoEngine(BaseTranslationEngine):
    NAME = "papago"
    VERSION = "1"

    def __init__(self):
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        if settings.papago_client_secret is None:
            raise TranslationEngineNotConfiguredError(
                f"{self.name_ver} engine: no client secret configured"
            )
        self.headers = (
            {
                "X-NCP-APIGW-API-KEY-ID": settings.papago_client_id,
                "X-NCP-APIGW-API-KEY": settings.papago_client_secret,
            }
            if settings.papago_naver_cloud
            else {
                "X-Naver-Client-Id": settings.papago_client_id,
                "X-Naver-Client-Secret": settings.papago_client_secret,
            }
        )
        self.endpoint = settings.papago_endpoint
        super().__init__()

    def get_supported_translations(self):
        #
        """
        Documentation https://docs.ncloud.com/en/naveropenapi_v3/translation/nmt.html specifies the following as of
        2020-06-05

        Korean (ko) 	→ 	English (en) 	            | 	English (en) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Japanese (ja) 	            | 	Japanese (ja) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Simplified Chinese (zh-CN) 	| 	Simplified Chinese (zh-CN) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Traditional Chinese (zh-TW) | 	Traditional Chinese (zh-TW) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Vietnamese (vi) 	        | 	Vietnamese (vi) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Indonesian (id) 	        | 	Indonesian (id) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Thai (th) 	                | 	Thai (th) 	→ 	Korean (ko)
        Korean (ko) 	→ 	German (de) 	            | 	German (de) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Russian (ru) 	            | 	Russian (ru) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Spanish (es) 	            | 	Spanish (es) 	→ 	Korean (ko)
        Korean (ko) 	→ 	Italian (it) 	            | 	Italian (it) 	→ 	Korean (ko)
        Korean (ko) 	→ 	French (fr) 	            |  	French (fr) 	→ 	Korean (ko)
        English (en) 	→ 	Japanese (ja) 	            | 	Japanese (ja) 	→ 	English (en)
        English (en) 	→ 	French (fr) 	            | 	French (fr) 	→ 	English (en)
        English (en) 	→ 	Simplified Chinese (zh-CN) 	| 	Simplified Chinese (zh-CN) 	→ 	English (en)
        English (en) 	→ 	Traditional Chinese (zh-TW) | 	Traditional Chinese (zh-TW) 	→ 	English (en)
        Japanese (ja) 	→ 	Simplified Chinese (zh-CN) 	| 	Simplified Chinese (zh-CN) 	→ 	Japanese (ja)
        Japanese (ja) 	→ 	Traditional Chinese (zh-TW) | 	Traditional Chinese (zh-TW) 	→ 	Japanese (ja)
        Simplified Chinese (zh-CN) 	→ 	Traditional Chinese (zh-TW) 	| 	Traditional Chinese (zh-TW) 	→ 	Simplified Chinese (zh-CN)
        """
        return {
            "ko": [
                "en",
                "ja",
                "zh-CN",
                "zh-TW",
                "vi",
                "id",
                "th",
                "de",
                "ru",
                "es",
                "it",
                "fr",
            ],
            "en": ["ja", "fr", "zh-CN", "zh-TW", "ko"],
            "zh-CN": ["ko", "zh-TW", "en", "ja"],
            "zh-TW": ["ko", "en", "zh-CN", "ja"],
            "ja": ["zh-CN", "zh-TW", "ko", "en"],
            "fr": ["ko", "en"],
            "es": ["ko"],
            "vi": ["ko"],
            "th": ["ko"],
            "id": ["ko"],
            "de": ["ko"],
            "it": ["ko"],
        }

    def handle_api_error(self, response_json: Dict[str, str]):
        if "errorCode" in response_json:
            raise EngineApiError(
                f"{self.name_ver} engine returned error code: {response_json['errorCode']},"
                f" message: {response_json['errorMessage']}"
            )

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
                self.endpoint,
                json={
                    "text": source_text,
                    "source": from_language,
                    "target": to_language,
                },
                headers={**self.headers, "Content-type": "application/json",},
            )
        response_json = response.json()
        self._logger.debug("%s got response: %s", self.name_ver, response_json)
        self.handle_api_error(response_json)
        try:
            translated_text = response_json["message"]["result"]["translatedText"]
        except KeyError as e:
            raise TranslationError(
                f"{self.name_ver} engine could not translate the given text"
            ) from e

        return TranslationResponse(
            engine=self.NAME,
            engine_version=self.VERSION,
            source_text=source_text,
            from_language=from_language,
            to_language=to_language,
            detected_language_confidence=None,
            translated_text=translated_text,
            alignment=None,
        )
