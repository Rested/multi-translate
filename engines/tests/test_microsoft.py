from engines.microsoft import parse_alignment_string, MicrosoftEngine


def test_with_documentation_example():
    """
    test with example from here
    https://docs.microsoft.com/en-gb/azure/cognitive-services/translator/reference/v3-0-translate
    """
    source_text = "The answer lies in machine translation."
    translated_text = "La réponse se trouve dans la traduction automatique."
    alignment_str = (
        "0:2-0:1 4:9-3:9 11:14-11:19 16:17-21:24 19:25-40:50 27:37-29:38 38:38-51:51"
    )
    result = parse_alignment_string(
        alignment_str=alignment_str,
        source_text=source_text,
        translation_text=translated_text,
    )

    assert result == [
        {
            "dest": {"end": 1, "start": 0, "text": "La"},
            "src": {"end": 2, "start": 0, "text": "The"},
        },
        {
            "dest": {"end": 9, "start": 3, "text": "réponse"},
            "src": {"end": 9, "start": 4, "text": "answer"},
        },
        {
            "dest": {"end": 19, "start": 11, "text": "se trouve"},
            "src": {"end": 14, "start": 11, "text": "lies"},
        },
        {
            "dest": {"end": 24, "start": 21, "text": "dans"},
            "src": {"end": 17, "start": 16, "text": "in"},
        },
        {
            "dest": {"end": 50, "start": 40, "text": "automatique"},
            "src": {"end": 25, "start": 19, "text": "machine"},
        },
        {
            "dest": {"end": 38, "start": 29, "text": "traduction"},
            "src": {"end": 37, "start": 27, "text": "translation"},
        },
        {
            "dest": {"end": 51, "start": 51, "text": "."},
            "src": {"end": 38, "start": 38, "text": "."},
        },
    ]


def test_retrieve_supported_languages(monkeypatch):
    monkeypatch.setenv("microsoft_translator_subscription_key", "doesnt matter here")
    m = MicrosoftEngine()
    assert "en" in m.supported_translations and "es" in m.supported_translations["en"]
    assert "es" in m.supported_translations and "en" in m.supported_translations["en"]
