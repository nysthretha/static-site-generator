import unittest

from markdowntoblocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_newlines(self):
        md = """
first block



second block




third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["first block", "second block", "third block"],
        )

    def test_strips_whitespace(self):
        md = "  hello  \n\n  world  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["hello", "world"])

    def test_single_block(self):
        md = "just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["just one block"])

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_heading_and_paragraph(self):
        md = """# Heading

A paragraph with some text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading", "A paragraph with some text."],
        )


if __name__ == "__main__":
    unittest.main()
