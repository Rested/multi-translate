import pytest

from engines.google import bcp_47_to_iso_639
from errors import InvalidISO6391CodeError


def test_bcp_47_to_iso_639_can_handle_iso_639_starting_codes_correctly():
    assert bcp_47_to_iso_639("en-GB-oed") == "en"


def test_bcp_47_to_iso_639_errors_for_iso_639_3_letter_codes():
    with pytest.raises(InvalidISO6391CodeError) as excinfo:
        bcp_47_to_iso_639("cel-gaulish")

    assert "3-letter" in str(excinfo)


def test_bcp_47_to_iso_639_errors_for_non_iso_codes():
    with pytest.raises(InvalidISO6391CodeError) as excinfo:
        bcp_47_to_iso_639("fake-language")

    assert "no ISO-639 component" in str(excinfo)
