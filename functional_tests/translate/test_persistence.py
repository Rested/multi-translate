import httpx
from random import randint
from functional_tests.translate.test_translate import translate_url
from time import sleep


def test_saves_repeated_request():
    rand_num = randint(0, 10 ** 100)

    request_data = {
        "from_language": "en",
        "to_language": "es",
        "source_text": f"hello {rand_num}",
        "preferred_engine": "amazon",
        "with_alignment": False,
    }
    resp = httpx.get(translate_url(), params=request_data)
    assert resp.status_code == 200
    result = resp.json()

    expected_result = {
        "translated_text": f"hola {rand_num}",
        "engine": "amazon",
        "engine_version": "2020-04-30",
        "from_language": "en",
        "to_language": "es",
        "source_text": f"hello {rand_num}",
        "detected_language_confidence": None,
        "alignment": None,
    }

    assert result == expected_result
    assert resp.headers["X-Translation-Source"] == "api"
    sleep(5)
    repeated_resp = httpx.get(translate_url(), params=request_data)
    repeated_result = repeated_resp.json()
    assert repeated_result == expected_result
    assert repeated_resp.headers["X-Translation-Source"] == "database"
