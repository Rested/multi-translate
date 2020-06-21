from typing import Dict, Optional, Union, List

import graphene
from fastapi import Query
from pydantic import BaseModel, validator

# from engines.controller import BEST, ENGINE_NAME_MAP

Alignment = List[Dict[str, Dict[str, Union[str, int]]]]


# class TranslationRequest(BaseModel):
#     source_text: str = Query(..., description="The text to be translated"),
#     to_language: str = Query(..., max_length=2,
#                              description="The ISO-639-1 code of the language to translate the text to"),
#     from_language: str = Query(None, max_length=2,
#                                description="The ISO-639-1 code of the language to translate the text from - if not"
#                                            "specified then detection will be attempted"),
#     preferred_engine: str = Query(BEST,
#                                   description=f"Which translation engine to use. Choices are "
#                                               f"{', '.join(list(ENGINE_NAME_MAP.keys()))} and {BEST}"),
#     with_alignment: bool = Query(False, description="Whether to return word alignment information or not"),
#     fallback: bool = Query(False, description="Whether to fallback to the best available engine if the preferred "
#                                               "engine does not succeed"),
#
#     @validator("from_language", "to_language")
#     def name_must_contain_space(cls, v):
#         if v is None:
#             return v
#
#         if len(v) != 2:
#             raise ValueError("must be a 2 letter ISO 639-1 code")
#
#         return v


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
