import pytest
from decouple import strtobool


def test_true_values():
    for item in ("Y", "YES", "T", "TRUE", "ON", "1"):
        assert strtobool(item)


def test_false_values():
    for item in ("N", "NO", "F", "FALSE", "OFF", "0"):
        assert strtobool(item) is False


def test_invalid():
    with pytest.raises(ValueError, match="Invalid truth value"):
        strtobool("MAYBE")

