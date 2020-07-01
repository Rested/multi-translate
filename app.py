import logging

import graphene
import sqlalchemy
from fastapi import BackgroundTasks, FastAPI, Query, Response
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp

from db import database, metadata
from engines.controller import BEST, ENGINE_NAME_MAP
from gql_query import GQLQuery
from models.request import TranslationRequest
from models.response import (
    TranslationResponse,
)
from settings import DatabaseSettings, Settings, FeaturesSettings
from translate import controller, do_translation

_logger = logging.getLogger(__name__)

features = FeaturesSettings()

with open("VERSION") as f:
    version = f.read()

app = FastAPI(
    title="multi-translate",
    description="Multi-Translate is a unified interface on top of various translate APIs providing optimal "
                "translations, persistence, fallback.",
    version=version,
)


@app.get("/", response_model=str)
async def ready() -> str:
    return "ready"


@app.on_event("startup")
async def startup():
    # logging
    log_level = Settings().log_level.name
    logging.basicConfig(level=log_level)
    _logger.setLevel(level=log_level)
    # database
    if features.enable_persistence:
        await database.connect()
        engine = sqlalchemy.create_engine(DatabaseSettings().postgres_dsn)
        metadata.create_all(engine)
    # controller
    controller.get_available_engines()


@app.on_event("shutdown")
async def shutdown():
    if features.enable_persistence:
        await database.disconnect()


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
    return await do_translation(
        background_tasks,
        response,
        source_text=source_text,
        to_language=to_language,
        from_language=from_language,
        preferred_engine=preferred_engine,
        with_alignment=with_alignment,
        fallback=fallback,
    )


if features.enable_gql:
    app.add_route(
        "/gql",
        GraphQLApp(schema=graphene.Schema(query=GQLQuery), executor_class=AsyncioExecutor),
    )
