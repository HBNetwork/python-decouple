import pytest
from decouple import strtobool


def test_true_values():
    true_list = ["y", "yes", "t", "true", "on", "1"]
    for item in true_list:
        assert strtobool(item) == 1


def test_false_values():
    false_list = ["n", "no", "f", "false", "off", "0"]
    for item in false_list:
        assert strtobool(item) == 0


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Invalid_Value_1", "invalid truth value Invalid_Value_1"),
        ("1nv4l1d_V4lu3_2", "invalid truth value 1nv4l1d_V4lu3_2"),
        ("invalid_value_3", "invalid truth value invalid_value_3"),
    ],
)
def test_eval(test_input, expected):
    with pytest.raises(ValueError) as execinfo:
        strtobool(test_input)
    assert str(execinfo.value) == expected
