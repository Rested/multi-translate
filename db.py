import databases
import sqlalchemy
from sqlalchemy import UniqueConstraint

from settings import DatabaseSettings


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
