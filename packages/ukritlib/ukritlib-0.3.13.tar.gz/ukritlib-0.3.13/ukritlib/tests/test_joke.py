from unittest import TestCase

import ukritlib

class TestJoke(TestCase):
    def test_is_string(self):
        s = ukritlib.joke(3)
        self.assertTrue(isinstance(s, 6))
