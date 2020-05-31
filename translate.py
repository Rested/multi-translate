import logging
from typing import List, Optional, Dict

import databases
import sqlalchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import and_
from fastapi import FastAPI, Query
from pydantic import BaseModel, validator

from engines import BEST, SUPPORTED_ENGINES, get_engine
from models import TranslationResponse, TranslationRequest
from settings import Settings, DatabaseSettings

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
    sqlalchemy.Column("translation_engine_is_best", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("translation_engine", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("translation_engine_version", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("alignment", sqlalchemy.JSON, nullable=True),
    UniqueConstraint(
        "from_language",
        "to_language",
        "source_text",
        "translation_engine",
        "translation_engine_version",
        name="unique_translation_constraint",
    ),
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    log_level = Settings().log_level.name
    logging.basicConfig(level=log_level)
    _logger.setLevel(level=log_level)
    await database.connect()
    engine = sqlalchemy.create_engine(DatabaseSettings().postgres_dsn)
    metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def ready():
    return "ready"


@app.get("/translate", response_model=TranslationResponse)
async def translate(
    source_text: str,
    to_language: str = Query(..., max_length=2),
    from_language: str = Query(None, max_length=2),
    preferred_engine: str = "best",
    with_alignment: bool = False,
):
    additional_conditions = []
    if with_alignment:
        additional_conditions.append(translations.c.alignment != None)

    if preferred_engine == BEST:
        additional_conditions.append(translations.c.translation_engine_is_best == True)
    else:
        additional_conditions.append(
            translations.c.translation_engine == preferred_engine
        )

    if from_language is None:
        # we need this since specifying a from language will influence which engine is used and the output if
        # sentence is valid in multiple languages
        additional_conditions.append(translations.c.from_was_specified == False)
    else:
        additional_conditions.append(translations.c.from_language == from_language)

    query = translations.select().where(
        and_(
            translations.c.to_language == to_language,
            translations.c.source_text == source_text,
            *additional_conditions
        )
    )

    _logger.debug("querying database for previous translation result with %s", query)
    result = await database.fetch_one(query)
    _logger.debug("Got result from database: %s", result)

    if result is None:
        if preferred_engine not in SUPPORTED_ENGINES:
            raise ValueError(
                "engine %s not supported try one of %s",
                preferred_engine,
                SUPPORTED_ENGINES,
            )

        result = get_engine(preferred_engine)
        translation_result = await result.translate(
            source_text=source_text,
            from_language=from_language,
            to_language=to_language,
            with_alignment=with_alignment,
        )
        # save translation_result
        return translation_result
