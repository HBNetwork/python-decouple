import pytest
from decouple import strtobool


@pytest.mark.parametrize("value", ("Y", "YES", "T", "TRUE", "ON", "1"))
def test_true_values(value):
    assert strtobool(value)


@pytest.mark.parametrize("value", ("N", "NO", "F", "FALSE", "OFF", "0"))
def test_false_values(value):
    assert strtobool(value) is False


def test_invalid():
    with pytest.raises(ValueError, match="Invalid truth value"):
        strtobool("MAYBE")

