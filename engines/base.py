from typing import Dict, List, Optional

from errors import (
    AlignmentNotSupportedError,
    DetectionNotSupportedError,
    UnsupportedLanguagePairError,
)


class BaseTranslationEngine:
    NAME: str = "base"
    VERSION: str = ""

    supports_alignment: bool = False
    supports_detection: bool = False

    @property
    def name_ver(self):
        return f"{self.NAME} ({self.VERSION})"

    def __init__(self):
        self.supported_translations: Dict[
            str, List[str]
        ] = self.get_supported_translations()

    def get_supported_translations(self):
        raise NotImplementedError("get supported translations must be implemented")

    def is_language_pair_supported(
        self, from_language: Optional[str], to_language: str
    ):
        if from_language is None:
            if to_language in {
                to_l
                for list_of_to_l in self.supported_translations.values()
                for to_l in list_of_to_l
            }:
                return
        else:
            try:
                if to_language in self.supported_translations[from_language]:
                    return
            except KeyError:
                pass
        raise UnsupportedLanguagePairError(
            f"{self.name_ver} does not support the language pair {from_language} to {to_language}"
        )

    async def translate(
        self,
        source_text: str,
        from_language: Optional[str],
        to_language: str,
        with_alignment: Optional[bool] = False,
    ):
        self.is_language_pair_supported(
            from_language=from_language, to_language=to_language
        )
        if not from_language and not self.supports_detection:
            raise DetectionNotSupportedError(
                f"{self.name_ver} engine does not support detection, please specify "
                f"from_language"
            )
        if with_alignment and not self.supports_alignment:
            raise AlignmentNotSupportedError(
                f"{self.name_ver} does not support alignment"
            )
