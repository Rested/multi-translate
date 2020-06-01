from engines.amazon import AmazonEngine
from engines.base import BaseTranslationEngine
from engines.google import GoogleEngine
from engines.microsoft import MicrosoftEngine

BEST = "best"

SUPPORTED_ENGINES = (
    BEST,
    MicrosoftEngine.NAME,
    GoogleEngine.NAME,
    AmazonEngine.NAME,
)  # YANDEX, PAPAGO, IBM, DEEP_L)


# todo: make this a controller with proper handling of best
def get_engine(engine_name: str) -> BaseTranslationEngine:
    if engine_name == BEST:
        # determine best
        return MicrosoftEngine()

    for e in (MicrosoftEngine, GoogleEngine, AmazonEngine):
        if e.NAME == engine_name:
            return e()
