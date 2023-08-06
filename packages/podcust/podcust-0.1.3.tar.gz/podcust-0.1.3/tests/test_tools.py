"""Tests for podcust common tools."""

import pytest
from podcust.tools import get_user_input


# Mock input funtion:
# https://stackoverflow.com/a/56301794


class MockInputFunction:
    def __init__(self, return_value=None):
        self.return_value = return_value
        self._orig_input_fn = __builtins__["input"]

    def _mock_input_fn(self, prompt):
        print(prompt + ": " + str(self.return_value))
        return self.return_value

    def __enter__(self):
        __builtins__["input"] = self._mock_input_fn

    def __exit__(self, type, value, traceback):
        __builtins__["input"] = self._orig_input_fn


class TestGetUserInput:
    def test_validation_succeeds(self):
        with MockInputFunction(return_value="abc123"):
            assert get_user_input("test") == "abc123"

    def test_raises_length_error(self):
        with MockInputFunction(return_value="2" * 33):
            with pytest.raises(ValueError) as exc:
                get_user_input("test")

            assert str(exc.value) == ("Only type up to 30 characters.")

    def test_raises_non_alphanumeric(self):
        with MockInputFunction(return_value="a\r"):
            with pytest.raises(ValueError) as exc:
                get_user_input("test")

            assert str(exc.value) == ("Only type alphanumeric latin characters.")
