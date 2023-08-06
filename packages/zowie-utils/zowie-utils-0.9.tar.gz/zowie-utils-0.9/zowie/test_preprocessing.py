import unittest

from .preprocessing import remove_ascii_emoji, unify_url, unify_email, remove_html


class PreprocessingTest(unittest.TestCase):
    def test_remove_ascii_emoji_basic(self):
        cases = [
            ("one", "one"),
            ("one :)", "one "),
            ("one :) two :( three", "one  two  three"),
        ]

        for text, expected in cases:
            self.assertEqual(remove_ascii_emoji(text), expected)

    def test_unify_url_basic(self):
        cases = [
            ("http://google.com", "URL"),
            ("one http://google.com", "one URL"),
            ("one https://google.com/a/b two", "one URL two"),
        ]

        for text, expected in cases:
            self.assertEqual(unify_url(text), expected)

    def test_unify_email_basic(self):
        cases = [
            ("test@test.com", "EMAIL"),
            ("test123@test.com", "EMAIL"),
            ("ala.ma.kota1234@test.com", "EMAIL"),
            ("one test@test.com", "one EMAIL"),
        ]

        for text, expected in cases:
            self.assertEqual(unify_email(text), expected)

    def test_remove_html(self):
        cases = [
            ("<p>Hello world</p>", "Hello world"),
            ("<p>Hello world</p>!!!", "Hello world!!!"),
            ("<b>Hello</b> world", "Hello world"),
        ]

        for text, expected in cases:
            self.assertEqual(remove_html(text), expected)
