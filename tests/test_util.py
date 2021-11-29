import pytest
from util import strtobool


def test_true_values():
    true_list = ["y", "yes", "t", "true", "on", "1"]
    for item in true_list:
        assert strtobool(item) == 1


def test_false_values():
    false_list = ["n", "no", "f", "false", "off", "0"]
    for item in false_list:
        assert strtobool(item) == 0


def test_invalid_value_text():
    invalid_list = ["Invalid_Value_1", "1nv4l1d_V4lu3_2", "Invalid_Value_3"]
    for value in invalid_list:
        with pytest.raises(ValueError, match="invalid truth value '%s'".format(value)):
            strtobool(value)
