class TranslationEngineNotConfiguredError(BaseException):
    """A problem with the configuration of the translation engine"""


class DetectionError(BaseException):
    """A problem detecting the language of an empty from request"""


class TranslationError(BaseException):
    """A problem performing or parsing the translation"""


class EngineApiError(BaseException):
    """An error reported by an api service"""


class UnsupportedLanguagePairError(BaseException):
    """The from to language pair is not supported"""


class InvalidISO6391CodeError(BaseException):
    """Is not a valid iso-639-1 code"""


class AlignmentNotSupportedError(BaseException):
    """Alignment is not supported for this language combination"""


class AlignmentError(BaseException):
    """Alignment failed despite being supported"""
