import logging
from typing import Optional

import databases
import graphene
import sqlalchemy
from databases.backends.postgres import Record
from fastapi import BackgroundTasks, FastAPI, Query, Response
from graphql.execution.executors.asyncio import AsyncioExecutor
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import and_
from starlette.graphql import GraphQLApp

from engines.controller import BEST, ENGINE_NAME_MAP, EngineController
from errors import BaseMultiTranslateError
from models.request import TranslationRequest
from models.response import (
    AlignmentSection,
    AlignmentTextPos,
    GQLTranslationResponse,
    TranslationResponse,
)
from settings import DatabaseSettings, Settings


_logger = logging.getLogger(__name__)

database = databases.Database(DatabaseSettings().postgres_dsn)

metadata = sqlalchemy.MetaData()

translations = sqlalchemy.Table(
    "translation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("from_was_specified", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column(
        "from_language", sqlalchemy.String, nullable=True
    ),  # iso 639-1 2 letter code
    sqlalchemy.Column(
        "to_language", sqlalchemy.String, nullable=False
    ),  # iso 639-1 2 letter code
    sqlalchemy.Column("source_text", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("translated_text", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("translation_engine", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("translation_engine_version", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("has_alignment_info", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("alignment", sqlalchemy.JSON, nullable=True),
    sqlalchemy.Column("detection_confidence", sqlalchemy.Float, nullable=True),
    UniqueConstraint(
        "from_language",
        "to_language",
        "source_text",
        "translation_engine",
        "translation_engine_version",
        "has_alignment_info",
        name="unique_translation_constraint",
    ),
)

with open("VERSION") as f:
    version = f.read()

app = FastAPI(
    title="multi-translate",
    description="Multi-Translate is a unified interface on top of various translate APIs providing optimal "
    "translations, persistence, fallback.",
    version=version,
)

controller = EngineController()


@app.on_event("startup")
async def startup():
    # logging
    log_level = Settings().log_level.name
    logging.basicConfig(level=log_level)
    _logger.setLevel(level=log_level)
    # database
    await database.connect()
    engine = sqlalchemy.create_engine(DatabaseSettings().postgres_dsn)
    metadata.create_all(engine)
    # controller
    controller.get_available_engines()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_model=str)
async def ready() -> str:
    return "ready"


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


@app.post("/translate", response_model=TranslationResponse)
async def translate_post(
    background_tasks: BackgroundTasks,
    response: Response,
    translation_request: TranslationRequest,
) -> TranslationResponse:
    return await translate(
        background_tasks,
        response,
        source_text=translation_request.source_text,
        to_language=translation_request.to_language,
        from_language=translation_request.from_language,
        preferred_engine=translation_request.preferred_engine,
        with_alignment=translation_request.with_alignment,
        fallback=translation_request.fallback,
    )


@app.get("/translate", response_model=TranslationResponse)
async def translate(
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
        background_tasks.add_task(
            save_translation, translation_result, from_language is not None
        )
        response.headers["X-Translation-Source"] = "api"
        return translation_result

    raise Exception(
        "no translation result or exception raised - this should never happen"
    )


class GQLQuery(graphene.ObjectType):
    translation = graphene.Field(
        GQLTranslationResponse,
        source_text=graphene.String(
            description="The text to be translated", required=True
        ),
        to_language=graphene.String(
            description="The ISO-639-1 code of the language to translate the text to",
            required=True,
        ),
        from_language=graphene.String(
            description="The ISO-639-1 code of the language to translate the text from - if not"
            "specified then detection will be attempted"
        ),
        preferred_engine=graphene.String(
            description=f"Which translation engine to use. Choices are "
            f"{', '.join(list(ENGINE_NAME_MAP.keys()))} and {BEST}"
        ),
        with_alignment=graphene.Boolean(
            description="Whether to return word alignment information or not"
        ),
        fallback=graphene.Boolean(
            description="Whether to fallback to the best available engine if the preferred "
            "engine does not succeed"
        ),
    )

    async def resolve_translation(
        self,
        info,
        source_text,
        to_language,
        from_language=None,
        preferred_engine=BEST,
        with_alignment=False,
        fallback=False,
    ) -> GQLTranslationResponse:
        bg_tasks = BackgroundTasks()
        result = await translate(
            bg_tasks,
            Response(),
            source_text,
            to_language,
            from_language,
            preferred_engine,
            with_alignment,
            fallback,
        )

        alignment = None
        if result.alignment:
            alignment = [
                AlignmentSection(
                    dest=AlignmentTextPos(
                        end=sect["dest"]["end"],
                        start=sect["dest"]["start"],
                        text=sect["dest"]["text"],
                    ),
                    src=AlignmentTextPos(
                        end=sect["src"]["end"],
                        start=sect["src"]["start"],
                        text=sect["src"]["text"],
                    ),
                )
                for sect in result.alignment
            ]

        # TODO: find a way to make this happen after the response is returned
        await bg_tasks()

        return GQLTranslationResponse(
            engine=result.engine,
            engine_version=result.engine_version,
            detected_language_confidence=result.detected_language_confidence,
            from_language=result.from_language,
            to_language=result.to_language,
            source_text=result.source_text,
            translated_text=result.translated_text,
            alignment=alignment,
        )


app.add_route(
    "/gql",
    GraphQLApp(schema=graphene.Schema(query=GQLQuery), executor_class=AsyncioExecutor),
)
