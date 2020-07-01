import logging
from typing import Optional

from databases.backends.postgres import Record
from fastapi import BackgroundTasks, Query, Response
from sqlalchemy.sql import and_

from db import database, translations
from engines.controller import BEST, ENGINE_NAME_MAP, EngineController
from errors import BaseMultiTranslateError
from models.response import (
    TranslationResponse,
)
from settings import FeaturesSettings

features = FeaturesSettings()

_logger = logging.getLogger(__name__)

controller = EngineController()


async def save_translation(
        translation_result: TranslationResponse, from_was_specified: bool
) -> None:
    statement = translations.insert().values(
        from_was_specified=from_was_specified,
        from_language=translation_result.from_language,
        to_language=translation_result.to_language,
        source_text=translation_result.source_text,
        translated_text=translation_result.translated_text,
        translation_engine=translation_result.engine,
        translation_engine_version=translation_result.engine_version,
        has_alignment_info=translation_result.alignment is not None,
        alignment=translation_result.alignment,
        detection_confidence=translation_result.detected_language_confidence,
    )
    result = await database.execute(statement)
    _logger.debug("insertion result %s", result)


async def do_translation(
        background_tasks: BackgroundTasks,
        response: Response,
        source_text: str = Query(..., description="The text to be translated"),
        to_language: str = Query(
            ...,
            max_length=2,
            description="The ISO-639-1 code of the language to translate the text to",
        ),
        from_language: str = Query(
            None,
            max_length=2,
            description="The ISO-639-1 code of the language to translate the text from - if not"
                        "specified then detection will be attempted",
        ),
        preferred_engine: str = Query(
            BEST,
            description=f"Which translation engine to use. Choices are "
                        f"{', '.join(list(ENGINE_NAME_MAP.keys()))} and {BEST}",
        ),
        with_alignment: bool = Query(
            False, description="Whether to return word alignment information or not"
        ),
        fallback: bool = Query(
            False,
            description="Whether to fallback to the best available engine if the preferred "
                        "engine does not succeed",
        ),
) -> TranslationResponse:
    additional_conditions = []
    if with_alignment:
        additional_conditions.append(translations.c.has_alignment_info == True)

    if from_language is None:
        # we need this since specifying a from language will influence which engine is used and the output if
        # sentence is valid in multiple languages
        additional_conditions.append(translations.c.from_was_specified == False)
    else:
        additional_conditions.append(translations.c.from_language == from_language)

    excluded_engines = []
    use_engine = preferred_engine
    translation_result = None
    while True:
        engine = controller.get_engine(
            name=use_engine,
            needs_alignment=with_alignment,
            needs_detection=from_language is None,
            from_language=from_language,
            to_language=to_language,
            exclude_engines=excluded_engines,
        )
        additional_conditions.append(translations.c.translation_engine == engine.NAME)

        if features.enable_persistence:
            query = translations.select().where(
                and_(
                    translations.c.to_language == to_language,
                    translations.c.source_text == source_text,
                    *additional_conditions,
                )
            )
            _logger.debug(
                "querying database for previous translation result with %s", query
            )
            result: Optional[Record] = await database.fetch_one(query)
            _logger.debug("Got result from database: %s", result)
        else:
            result = None

        if result is None:
            try:
                translation_result = await engine.translate(
                    source_text=source_text,
                    from_language=from_language,
                    to_language=to_language,
                    with_alignment=with_alignment,
                )
            except BaseMultiTranslateError as e:
                _logger.debug("%s", e.detail, exc_info=True)
                if fallback:
                    # if an engine was specified we switch to fallback if the preferred failed
                    use_engine = BEST
                    excluded_engines.append(engine.NAME)
                    continue
                raise e
            break
        else:
            response.headers["X-Translation-Source"] = "database"
            return TranslationResponse(
                engine=result["translation_engine"],
                engine_version=result["translation_engine_version"],
                detection_confidence=result["detection_confidence"],
                from_language=result["from_language"],
                to_language=result["to_language"],
                source_text=result["source_text"],
                translated_text=result["translated_text"],
                alignment=result["alignment"] if with_alignment else None,
            )

    if translation_result:
        # save translation_result
        if features.enable_persistence:
            background_tasks.add_task(
                save_translation, translation_result, from_language is not None
            )
        response.headers["X-Translation-Source"] = "api"
        return translation_result

    raise Exception(
        "no translation result or exception raised - this should never happen"
    )
