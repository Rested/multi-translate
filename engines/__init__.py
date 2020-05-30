from engines.base import BaseTranslationEngine
from engines.microsoft import MicrosoftEngine

BEST = "best"

SUPPORTED_ENGINES = (
    BEST,
    MicrosoftEngine.NAME,
)  # GOOGLE, YANDEX, PAPAGO, AMAZON, IBM, DEEP_L)


def get_engine(engine_name: str) -> BaseTranslationEngine:
    if engine_name == BEST:
        # determine best
        return MicrosoftEngine()

    for e in (MicrosoftEngine,):
        return e()
