from typing import Dict, Optional, Union, List

from pydantic import BaseModel, validator

Alignment = List[Dict[str, Dict[str, Union[str, int]]]]


class TranslationRequest(BaseModel):
    from_language: Optional[str] = None
    to_language: str
    source_text: str
    preferred_engine: Optional[str] = "best"
    with_alignment: Optional[bool] = False

    @validator("from_language", "to_language")
    def name_must_contain_space(cls, v):
        if v is None:
            return v

        if len(v) != 2:
            raise ValueError("must be a 2 letter ISO 639-1 code")

        return v


class TranslationResponse(BaseModel):
    engine: str
    engine_version: str
    detected_language_confidence: Optional[float]  # between 0 and 1 - 1 is most
    from_language: str
    to_language: str
    source_text: str
    translated_text: str
    alignment: Optional[Alignment]

    class Config:
        schema_extra = {
            "example": {
                "translated_text": "안녕하세요",
                "engine": "microsoft",
                "engine_version": "3.0",
                "from_language": "en",
                "to_language": "ko",
                "source_text": "hello",
                "detected_language_confidence": None,
                "alignment": [
                    {
                        "dest": {"end": "4", "start": "0", "text": "안녕하세요"},
                        "src": {"end": "4", "start": "0", "text": "hello"},
                    }
                ],
            }
        }
