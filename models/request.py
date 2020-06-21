from fastapi import Query
from pydantic import BaseModel

from engines.controller import BEST, ENGINE_NAME_MAP


class TranslationRequest(BaseModel):
    source_text: str = Query(..., description="The text to be translated")
    to_language: str = Query(..., max_length=2,
                             description="The ISO-639-1 code of the language to translate the text to")
    from_language: str = Query(None, max_length=2,
                               description="The ISO-639-1 code of the language to translate the text from - if not"
                                           "specified then detection will be attempted")
    preferred_engine: str = Query(BEST,
                                  description=f"Which translation engine to use. Choices are "
                                              f"{', '.join(list(ENGINE_NAME_MAP.keys()))} and {BEST}")
    with_alignment: bool = Query(False, description="Whether to return word alignment information or not")
    fallback: bool = Query(False, description="Whether to fallback to the best available engine if the preferred "
                                              "engine does not succeed")
