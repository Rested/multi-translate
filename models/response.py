from typing import List, Dict, Union, Optional

import graphene
from pydantic import BaseModel

Alignment = List[Dict[str, Dict[str, Union[str, int]]]]


class AlignmentTextPos(graphene.ObjectType):
    end = graphene.Int()
    start = graphene.Int()
    text = graphene.String()


class AlignmentSection(graphene.ObjectType):
    dest = graphene.Field(AlignmentTextPos, required=True)
    src = graphene.Field(AlignmentTextPos, required=True)


class GQLTranslationResponse(graphene.ObjectType):
    engine = graphene.String()
    engine_version = graphene.String()
    detected_language_confidence = graphene.Float()
    from_language = graphene.String()
    to_language = graphene.String()
    source_text = graphene.String()
    translated_text = graphene.String()
    alignment = graphene.List(of_type=AlignmentSection)


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