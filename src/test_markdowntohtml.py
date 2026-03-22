import unittest

from markdowntohtml import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_quote(self):
        md = """
> This is a
> blockquote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item **two**
- item three
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_heading_with_inline(self):
        md = """
# Hello **bold** and _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Hello <b>bold</b> and <i>italic</i></h1></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Title

A paragraph with a [link](https://example.com).

- list item
- another item

> a quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><p>A paragraph with a <a href="https://example.com">link</a>.</p><ul><li>list item</li><li>another item</li></ul><blockquote>a quote</blockquote></div>',
        )

    def test_image_in_paragraph(self):
        md = """
Here is an ![alt](https://example.com/img.png) in text.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Here is an <img src="https://example.com/img.png" alt="alt"></img> in text.</p></div>',
        )


if __name__ == "__main__":
    unittest.main()
