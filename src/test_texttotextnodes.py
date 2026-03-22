import unittest

from textnode import TextNode, TextType
from texttotextnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_plain_text(self):
        nodes = text_to_textnodes("just plain text")
        self.assertListEqual([TextNode("just plain text", TextType.TEXT)], nodes)

    def test_bold_only(self):
        nodes = text_to_textnodes("**bold**")
        self.assertListEqual([TextNode("bold", TextType.BOLD)], nodes)

    def test_italic_only(self):
        nodes = text_to_textnodes("_italic_")
        self.assertListEqual([TextNode("italic", TextType.ITALIC)], nodes)

    def test_code_only(self):
        nodes = text_to_textnodes("`code`")
        self.assertListEqual([TextNode("code", TextType.CODE)], nodes)

    def test_image_only(self):
        nodes = text_to_textnodes("![alt](https://example.com/img.png)")
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
            nodes,
        )

    def test_link_only(self):
        nodes = text_to_textnodes("[click](https://example.com)")
        self.assertListEqual(
            [TextNode("click", TextType.LINK, "https://example.com")],
            nodes,
        )

    def test_multiple_bold(self):
        nodes = text_to_textnodes("**one** and **two**")
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            nodes,
        )

    def test_adjacent_types(self):
        nodes = text_to_textnodes("**bold**_italic_`code`")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
