from typing import Optional

from fastapi import HTTPException


class BaseMultiTranslateError(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=400, detail=detail, headers={})


class TranslationEngineNotConfiguredError(BaseMultiTranslateError):
    """A problem with the configuration of the translation engine"""


class DetectionError(BaseMultiTranslateError):
    """A problem detecting the language of an empty from_language request"""


class DetectionNotSupportedError(BaseMultiTranslateError):
    """Detection is not supported for this engine"""


class TranslationError(BaseMultiTranslateError):
    """A problem performing or parsing the translation"""


class EngineApiError(BaseMultiTranslateError):
    """An error reported by an api service"""


class UnsupportedLanguagePairError(BaseMultiTranslateError):
    """The from to language pair is not supported"""


class InvalidISO6391CodeError(BaseMultiTranslateError):
    """Is not a valid iso-639-1 code"""


class AlignmentNotSupportedError(BaseMultiTranslateError):
    """Alignment is not supported for this language combination"""


class AlignmentError(BaseMultiTranslateError):
    """Alignment failed despite being supported"""
