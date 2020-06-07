from engines.amazon import AmazonEngine
from engines.base import BaseTranslationEngine
from engines.deep_l import DeepLEngine
from engines.google import GoogleEngine
from engines.microsoft import MicrosoftEngine
from engines.papago import PapagoEngine
from engines.yandex import YandexEngine

BEST = "best"

SUPPORTED_ENGINES = (
    BEST,
    MicrosoftEngine.NAME,
    GoogleEngine.NAME,
    AmazonEngine.NAME,
    PapagoEngine.NAME,
    DeepLEngine.NAME,
    YandexEngine.NAME
)  # IBM


# todo: make this a controller with proper handling of best
def get_engine(engine_name: str) -> BaseTranslationEngine:
    if engine_name == BEST:
        # determine best
        return MicrosoftEngine()

    for e in (MicrosoftEngine, GoogleEngine, AmazonEngine, PapagoEngine, DeepLEngine, YandexEngine):
        if e.NAME == engine_name:
            return e()
