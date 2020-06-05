from engines.amazon import AmazonEngine
from engines.base import BaseTranslationEngine
from engines.google import GoogleEngine
from engines.microsoft import MicrosoftEngine
from engines.papago import PapagoEngine

BEST = "best"

SUPPORTED_ENGINES = (
    BEST,
    MicrosoftEngine.NAME,
    GoogleEngine.NAME,
    AmazonEngine.NAME,
    PapagoEngine.NAME,
)  # YANDEX, PAPAGO, IBM, DEEP_L)


# todo: make this a controller with proper handling of best
def get_engine(engine_name: str) -> BaseTranslationEngine:
    if engine_name == BEST:
        # determine best
        return MicrosoftEngine()

    for e in (MicrosoftEngine, GoogleEngine, AmazonEngine, PapagoEngine):
        if e.NAME == engine_name:
            return e()
