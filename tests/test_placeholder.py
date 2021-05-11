from jeroenbos.partest import code
from unittest import TestCase


class TestTypeguard(TestCase):
    def test_typeguard_hook(self):
        """
        All code in `./src` is typeguarded when called from `./tests`.
        This test asserts that hook is established.

        Note that mypy(v0.812) nor Pylance(v2021.5.1) complain when passing a string to a function that expects an int.
        The library typeguard throws at runtime.
        """
        with self.assertRaises(TypeError):
            code.give_me_an_int("")
