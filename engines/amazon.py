import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from engines.base import BaseTranslationEngine
from errors import DetectionNotSupportedError, TranslationEngineNotConfiguredError, AlignmentNotSupportedError, \
    TranslationError, EngineApiError
from models import TranslationResponse
from settings import Settings


class AmazonEngine(BaseTranslationEngine):
    NAME = "amazon"
    # see https://docs.aws.amazon.com/translate/latest/dg/doc-history.html rolling version history
    # version below is the date of the latest change that would affect either the features or languages supported that
    # has been updated in this code
    VERSION = "2020-04-30"
    # retrieved from https://docs.aws.amazon.com/translate/latest/dg/what-is.html on 2020-06-01
    LANGUAGES = {"af", "sq", "am", "ar", "az", "bn", "bs", "bg", "zh",
                 "hr", "cs", "da", "fa",
                 "nl", "en", "et", "fi", "fr",
                 "ka", "de", "el", "ha", "he", "hi", "hu", "id", "it", "ja", "ko", "lv", "ms", "no", "fa",
                 "ps", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "so", "es", "es",
                 "sw", "sv", "tl", "ta", "th", "tr", "uk", "ur", "vi"}

    def __init__(self):
        settings = Settings()
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(settings.log_level.value)
        if settings.aws_secret_access_key is None or settings.aws_access_key_id is None:
            raise TranslationEngineNotConfiguredError(f"{self.name_ver} not configured correctly, "
                                                      f"aws_secret_access_key and aws_access_key_id must be set")
        self.client = self.get_client(settings.amazon_region)
        super().__init__()

    def get_supported_translations(self):
        return {language: self.LANGUAGES for language in self.LANGUAGES}

    def get_client(self, region: Optional[str]):
        if region is None:
            raise TranslationEngineNotConfiguredError(f"{self.name_ver} not configured correctly, amazon_region must be"
                                                      f" specified")
        return boto3.client(service_name='translate', region_name=region, use_ssl=True)

    async def translate(
            self,
            source_text: str,
            from_language: Optional[str],
            to_language: str,
            with_alignment: Optional[bool] = False,
    ) -> TranslationResponse:
        await super().translate(source_text=source_text, to_language=to_language, from_language=from_language,
                                with_alignment=with_alignment)

        try:
            result = self.client.translate_text(Text=source_text,
                                                SourceLanguageCode=from_language, TargetLanguageCode=to_language)
        except ClientError as e:
            raise EngineApiError(f"{self.name_ver} had a problem making translate api request") from e
        self._logger.debug("%s got response: %s", self.name_ver, result)

        try:
            translated_text = result["TranslatedText"]
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
