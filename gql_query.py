import typing

import graphene
from starlette.background import BackgroundTasks
from starlette.graphql import GraphQLApp
from starlette.responses import Response

from engines.controller import BEST, ENGINE_NAME_MAP
from models.request import TranslationRequest
from models.response import (
    AlignmentSection,
    AlignmentTextPos,
    GQLTranslationResponse,
)
from translate import do_translation


class RateLimGQLApp(GraphQLApp):
    def __init__(
        self,
        schema: "graphene.Schema",
        executor: typing.Any = None,
        executor_class: type = None,
        graphiql: bool = True,
        limits_decorator: typing.Optional[typing.Callable] = None,
    ) -> None:
        super().__init__(
            schema, executor, executor_class=executor_class, graphiql=graphiql
        )
        if limits_decorator:
            self.handle_graphiql = limits_decorator(self.handle_graphiql)
            self.handle_graphql = limits_decorator(self.handle_graphql)


class GQLQuery(graphene.ObjectType):
    translation = graphene.Field(
        GQLTranslationResponse,
        source_text=graphene.String(
            description="The text to be translated", required=True,
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
        # validate
        TranslationRequest(
            source_text=source_text,
            to_language=to_language,
            from_language=from_language,
            preferred_engine=preferred_engine,
            with_alignment=with_alignment,
            fallback=fallback,
        )
        result = await do_translation(
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
