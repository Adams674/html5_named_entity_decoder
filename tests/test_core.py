"""Tests for html5_named_entity_decoder.core."""
import unittest

from html5_named_entity_decoder.core import (
    decode,
    decode_entities,
    NAMED_REFERENCES,
)


class TestDecode(unittest.TestCase):
    def test_basic_semicolon_entity(self):
        self.assertEqual(decode("&amp;"), "&")

    def test_entity_inside_text(self):
        self.assertEqual(decode("a &amp; b"), "a & b")

    def test_multiple_entities(self):
        self.assertEqual(decode("&lt;&gt;&amp;"), "<>&")

    def test_legacy_no_semicolon_amp(self):
        # &amp without semicolon is a valid legacy entity.
        self.assertEqual(decode("Tom &amp Jerry"), "Tom & Jerry")

    def test_legacy_no_semicolon_copy(self):
        self.assertEqual(decode("&copy 2021"), "\u00a9 2021")

    def test_longest_match_wins(self):
        # &amp; should match as a whole, not as &amp followed by stray ';'.
        self.assertEqual(decode("x&amp;y"), "x&y")

    def test_ampersand_with_no_match_is_preserved(self):
        # &unknown; is not a named entity; the raw text is kept.
        self.assertEqual(decode("&unknown;"), "&unknown;")

    def test_bare_ampersand_preserved(self):
        self.assertEqual(decode("a & b"), "a & b")

    def test_empty_string(self):
        self.assertEqual(decode(""), "")

    def test_no_entities(self):
        self.assertEqual(decode("plain text"), "plain text")

    def test_numeric_reference_not_decoded(self):
        # Per the documented scope, numeric refs are left alone.
        self.assertEqual(decode("&#65;"), "&#65;")

    def test_decode_entities_alias(self):
        self.assertIs(decode_entities, decode)
        self.assertEqual(decode_entities("&lt;"), "<")

    def test_named_references_table_populated(self):
        # Sanity: the table contains canonical entries.
        self.assertIn("&amp;", NAMED_REFERENCES)
        self.assertEqual(NAMED_REFERENCES["&amp;"], "&")
        self.assertIn("&copy;", NAMED_REFERENCES)

    def test_adjacent_entities(self):
        self.assertEqual(decode("&amp;&amp;"), "&&")

    def test_entity_at_start_and_end(self):
        self.assertEqual(decode("&lt;middle&gt;"), "<middle>")


if __name__ == "__main__":
    unittest.main()
