import unittest

from extracttitle import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_trailing_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_with_other_content(self):
        md = """# My Title

Some paragraph text here.

## A subheading
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_h1_not_first_line(self):
        md = """Some intro text

# The Title

More text
"""
        self.assertEqual(extract_title(md), "The Title")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Not an h1\n\nSome text")

    def test_no_heading_at_all_raises(self):
        with self.assertRaises(ValueError):
            extract_title("just a paragraph")

    def test_ignores_h2(self):
        md = """## Subheading

# Actual Title
"""
        self.assertEqual(extract_title(md), "Actual Title")


if __name__ == "__main__":
    unittest.main()
